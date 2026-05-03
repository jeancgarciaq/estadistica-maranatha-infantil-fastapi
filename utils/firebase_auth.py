import json
import logging
import os
import time
import sys

# Añadir el directorio raíz del proyecto a la ruta de Python para resolver importaciones de modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataclasses import dataclass
from types import SimpleNamespace
from urllib import error, parse, request

from models.security import DEFAULT_ROLE_PERMISSIONS, ROLE_ROOT

logger = logging.getLogger(__name__)


@dataclass
class FirebaseAuthSession:
    local_id: str
    email: str
    id_token: str
    refresh_token: str
    expires_at: float


class FirebaseAuthService:
    """Autenticación Firebase con email/password + resolución de rol en Realtime Database."""

    def __init__(self, api_key=None, database_url=None, email_domain=None, timeout=15):
        # Busca tanto FIREBASE_API_KEY como FIREBASE_WEB_API_KEY para mayor flexibilidad
        self.api_key = api_key or os.getenv('FIREBASE_API_KEY') or os.getenv('FIREBASE_WEB_API_KEY', '').strip()
        self.database_url = (database_url or os.getenv('FIREBASE_DATABASE_URL', '')).rstrip('/')
        self.email_domain = (email_domain or os.getenv('FIREBASE_AUTH_EMAIL_DOMAIN', '')).strip().lower()
        self.timeout = timeout

    def reconstruct_session(self, id_token, local_id=None, email=None):
        """
        Reconstruye un objeto de sesión a partir de datos persistidos (ej. cookies).
        Útil para el middleware de FastAPI.
        """
        if not id_token:
            return None
        return FirebaseAuthSession(
            local_id=local_id or "",
            email=email or "",
            id_token=id_token,
            refresh_token="",  # No disponible en reconstrucción simple
            expires_at=time.time() + 3600
        )

    def is_configured(self):
        return bool(self.api_key and self.database_url)

    def sign_in(self, username_or_email, password):
        if not self.api_key:
            raise RuntimeError('FIREBASE_WEB_API_KEY no está configurado.')

        email = self._resolve_email(username_or_email)
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True,
        }

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        response = self._post_json(url, payload)

        return FirebaseAuthSession(
            local_id=response['localId'],
            email=response.get('email', email),
            id_token=response['idToken'],
            refresh_token=response['refreshToken'],
            expires_at=time.time() + int(response.get('expiresIn', '3600')),
        )

    def refresh(self, session):
        if not self.api_key:
            raise RuntimeError('FIREBASE_WEB_API_KEY no está configurado.')

        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        body = parse.urlencode({'grant_type': 'refresh_token', 'refresh_token': session.refresh_token}).encode('utf-8')
        req = request.Request(url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            payload = exc.read().decode('utf-8', errors='ignore')
            raise RuntimeError(self._build_auth_error(payload)) from exc
        except error.URLError as exc:
            raise RuntimeError(f'Error de conexión al refrescar token Firebase: {exc.reason}') from exc

        session.id_token = data['id_token']
        session.refresh_token = data.get('refresh_token', session.refresh_token)
        session.expires_at = time.time() + int(data.get('expires_in', '3600'))
        session.local_id = data.get('user_id', session.local_id)
        return session

    def get_valid_id_token(self, session):
        if session.expires_at - time.time() < 60:
            self.refresh(session)
        return session.id_token

    def fetch_role_assignment(self, session):
        if not self.database_url:
            raise RuntimeError('FIREBASE_DATABASE_URL no está configurado.')

        token = self.get_valid_id_token(session)
        path = f"{self.database_url}/user_roles/{session.local_id}.json"
        url = f"{path}?{parse.urlencode({'auth': token})}"

        req = request.Request(url, method='GET')
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode('utf-8')
                data = json.loads(raw) if raw else None
        except error.HTTPError as exc:
            payload = exc.read().decode('utf-8', errors='ignore')
            raise RuntimeError(f'No se pudo leer rol Firebase: {payload}') from exc
        except error.URLError as exc:
            raise RuntimeError(f'Error de conexión consultando rol Firebase: {exc.reason}') from exc

        if not data:
            raise RuntimeError('Usuario autenticado sin rol asignado en /user_roles/{uid}.')

        role_name = (data.get('role') or '').strip().lower()
        active = bool(data.get('active', True))
        display_name = (data.get('username') or session.email or '').strip()

        if not role_name:
            raise RuntimeError('El rol del usuario en Firebase está vacío.')

        if role_name not in DEFAULT_ROLE_PERMISSIONS:
            raise RuntimeError(f"Rol '{role_name}' no reconocido por la aplicación.")

        return {
            'role': role_name,
            'active': active,
            'username': display_name,
        }

    def build_runtime_user(self, session, role_assignment):
        role_name = role_assignment['role']
        permisos = []
        for code in DEFAULT_ROLE_PERMISSIONS.get(role_name, []):
            permisos.append(SimpleNamespace(codigo=code))

        role = SimpleNamespace(nombre=role_name, permisos=permisos)
        username = role_assignment.get('username') or session.email

        return SimpleNamespace(
            id=session.local_id,
            username=username,
            activo=role_assignment.get('active', True),
            rol=role,
            firebase_session=session,
            is_firebase_user=True,
        )

    def _resolve_email(self, username_or_email):
        user = (username_or_email or '').strip().lower()
        if '@' in user:
            return user
        if self.email_domain:
            return f"{user}@{self.email_domain}"
        return user

    def _post_json(self, url, payload):
        req = request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='ignore')
            raise RuntimeError(self._build_auth_error(body)) from exc
        except error.URLError as exc:
            raise RuntimeError(f'Error de conexión en Firebase Auth: {exc.reason}') from exc

    def _build_auth_error(self, payload):
        try:
            data = json.loads(payload)
            code = data.get('error', {}).get('message', 'AUTH_ERROR')
        except Exception:
            return f'Error de autenticación Firebase: {payload}'

        messages = {
            'EMAIL_NOT_FOUND': 'Usuario no registrado en Firebase Auth.',
            'INVALID_PASSWORD': 'Contraseña inválida.',
            'USER_DISABLED': 'Usuario deshabilitado en Firebase Auth.',
            'INVALID_LOGIN_CREDENTIALS': 'Credenciales inválidas.',
            'TOKEN_EXPIRED': 'Sesión expirada, inicie sesión nuevamente.',
            'INVALID_REFRESH_TOKEN': 'No se pudo refrescar la sesión del usuario.',
        }
        return messages.get(code, f'Error Firebase Auth: {code}')