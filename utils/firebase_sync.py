import json
import logging
import os
import uuid
from datetime import date, datetime
from decimal import Decimal
from urllib import error, parse, request

from sqlalchemy.inspection import inspect
from sqlalchemy.sql.sqltypes import Date as SQLDate
from sqlalchemy.sql.sqltypes import DateTime as SQLDateTime

from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.areas import Area
from models.aulas import Aula
from models.donaciones import Donacion
from models.distribucion import Distribucion
from models.ensenanza import Ensenanza
from models.logistica import Logistica
from models.otras_areas import OtrasAreas
from models.recepcion import Recepcion
from models.salones import Salon
from models.security import Permiso, Rol, Usuario
from models.sync_queue import SyncQueue

logger = logging.getLogger(__name__)


MODEL_REGISTRY = {
    'donaciones': Donacion,
    'distribuciones': Distribucion,
    'usuarios': Usuario,
}


class FirebaseClient:
    """Cliente simple para Firebase Realtime Database via REST."""

    def __init__(self, database_url=None, auth_token=None, token_provider=None, timeout=15):
        self.database_url = (database_url or os.getenv('FIREBASE_DATABASE_URL', '')).rstrip('/')
        self.auth_token = auth_token or os.getenv('FIREBASE_AUTH_TOKEN')
        self.token_provider = token_provider
        self.timeout = timeout

    def is_configured(self):
        return bool(self.database_url)

    def _build_url(self, path, auth_token=None):
        base_path = path.strip('/')
        url = f"{self.database_url}/{base_path}.json"
        params = {}
        resolved_token = auth_token
        if resolved_token is None and callable(self.token_provider):
            resolved_token = self.token_provider()
        if resolved_token is None:
            resolved_token = self.auth_token
        if resolved_token:
            params['auth'] = resolved_token
        if params:
            url = f"{url}?{parse.urlencode(params)}"
        return url

    def _request(self, method, path, payload=None, auth_token=None):
        if not self.is_configured():
            raise RuntimeError('Firebase database URL not configured.')

        data = None
        headers = {'Content-Type': 'application/json'}
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

        req = request.Request(self._build_url(path, auth_token=auth_token), data=data, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode('utf-8')
                return json.loads(raw) if raw else None
        except error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='ignore')
            raise RuntimeError(f'Firebase HTTP error {exc.code}: {body}') from exc
        except error.URLError as exc:
            raise RuntimeError(f'Firebase connection error: {exc.reason}') from exc

    def get(self, path, auth_token=None):
        return self._request('GET', path, auth_token=auth_token)

    def put(self, path, payload, auth_token=None):
        return self._request('PUT', path, payload, auth_token=auth_token)

    def patch(self, path, payload, auth_token=None):
        return self._request('PATCH', path, payload, auth_token=auth_token)

    def delete(self, path, auth_token=None):
        return self._request('DELETE', path, auth_token=auth_token)


class SyncManager:
    """Gestiona cola local y sincronización piloto con Firebase."""

    def __init__(self, client=None, device_id=None):
        self.client = client or FirebaseClient()
        self.device_id = device_id or os.getenv('SYNC_DEVICE_ID') or str(uuid.uuid4())

    def set_auth_token_provider(self, provider):
        self.client.token_provider = provider

    def queue_path(self, entity_name, entity_sync_id):
        return f"collections/{entity_name}/{entity_sync_id}"

    def collection_path(self, entity_name):
        return f"collections/{entity_name}"

    def enqueue_model(self, session, entity_name, registry_object, operation='upsert'):
        payload = self.serialize_model(registry_object)
        payload['sync_device_id'] = self.device_id
        payload['sync_operation'] = operation
        payload['sync_entity_name'] = entity_name

        event = SyncQueue()
        setattr(event, 'entity_name', entity_name)
        setattr(event, 'entity_sync_id', payload['sync_id'])
        setattr(event, 'operation', operation)
        setattr(event, 'payload_json', json.dumps(payload, ensure_ascii=False))
        setattr(event, 'status', 'pending')
        session.add(event)
        return event

    def serialize_model(self, record):
        mapper = inspect(record.__class__)
        data = {}
        for column in mapper.columns:
            value = getattr(record, column.key)
            data[column.key] = self._json_safe_value(value)
        return data

    def _json_safe_value(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, Decimal):
            return float(value)
        return value

    def push_pending(self, session):
        if not self.client.is_configured():
            return []

        pushed = []
        events = (
            session.query(SyncQueue)
            .filter(SyncQueue.status == 'pending')
            .order_by(SyncQueue.id.asc())
            .all()
        )

        for event in events:
            payload = json.loads(event.payload_json)
            try:
                remote_payload = dict(payload)
                remote_payload['sync_pushed_at'] = datetime.utcnow().isoformat()
                path = self.queue_path(event.entity_name, event.entity_sync_id)
                self.client.put(path, remote_payload)
                event.status = 'synced'
                event.last_error = None
                event.processed_at = datetime.utcnow()
                pushed.append(event.id)
            except Exception as exc:
                event.status = 'failed'
                event.attempts = (event.attempts or 0) + 1
                event.last_error = str(exc)
                logger.exception('No se pudo sincronizar evento %s', event.id)

        session.commit()
        return pushed

    def pull_collection(self, session, entity_name):
        if not self.client.is_configured():
            return []

        model = MODEL_REGISTRY.get(entity_name)
        if model is None:
            raise ValueError(f'Entidad no soportada para sincronización: {entity_name}')

        remote_data = self.client.get(self.collection_path(entity_name))
        if not remote_data:
            return []

        updated = []
        for entity_sync_id, payload in remote_data.items():
            if not isinstance(payload, dict):
                continue

            local = session.query(model).filter(model.sync_id == entity_sync_id).first()
            if local is None:
                local = model()
                session.add(local)

            self._apply_payload(local, payload)
            updated.append(entity_sync_id)

        session.commit()
        return updated

    def _apply_payload(self, record, payload):
        mapper = inspect(record.__class__)
        columns = {column.key: column for column in mapper.columns}

        for key, value in payload.items():
            column = columns.get(key)
            if column is None:
                continue

            setattr(record, key, self._coerce_value(column.type, value))

    def _coerce_value(self, column_type, value):
        if value is None:
            return None

        if isinstance(column_type, SQLDate) and isinstance(value, str):
            return date.fromisoformat(value)
        if isinstance(column_type, SQLDateTime) and isinstance(value, str):
            return datetime.fromisoformat(value)
        return value