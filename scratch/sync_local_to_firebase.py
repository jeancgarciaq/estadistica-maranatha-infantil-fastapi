import argparse
import logging
import os
import sys

# Permite ejecutar el script desde /scratch sin errores de import.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import SessionLocal, configure_database
from utils.env_loader import load_app_env
from utils.firebase_sync import MODEL_REGISTRY, SYNC_COLLECTION_ORDER, SyncManager
from utils.firebase_auth import FirebaseAuthService


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Sube registros existentes de SQLite a Firebase Realtime Database.'
    )
    parser.add_argument(
        '--collections',
        nargs='+',
        default=SYNC_COLLECTION_ORDER,
        help='Colecciones a sincronizar. Ejemplo: --collections areas salones aulas ...',
    )
    return parser.parse_args()


def _resolve_auth_token(requested_collections):
    """Resuelve token de escritura para Realtime Database."""
    explicit_token = (os.getenv('FIREBASE_AUTH_TOKEN') or '').strip()
    if explicit_token:
        return explicit_token

    login_name = (
        os.getenv('FIREBASE_BOOTSTRAP_EMAIL')
        or os.getenv('FIREBASE_BOOTSTRAP_USERNAME')
        or ''
    ).strip()
    login_password = (os.getenv('FIREBASE_BOOTSTRAP_PASSWORD') or '').strip()

    if not login_name or not login_password:
        raise RuntimeError(
            'Define FIREBASE_AUTH_TOKEN o FIREBASE_BOOTSTRAP_EMAIL/FIREBASE_BOOTSTRAP_PASSWORD '
            'para autenticar la sincronizacion inicial.'
        )

    auth = FirebaseAuthService()
    if not auth.is_configured():
        raise RuntimeError('FIREBASE_WEB_API_KEY y FIREBASE_DATABASE_URL son requeridos para autenticar bootstrap.')

    auth_session = auth.sign_in(login_name, login_password)
    role_assignment = auth.fetch_role_assignment(auth_session)

    if not role_assignment.get('active', True):
        raise RuntimeError('El usuario de bootstrap existe pero esta desactivado en user_roles.')

    role = (role_assignment.get('role') or '').strip().lower()
    needs_admin = 'usuarios' in requested_collections
    if needs_admin and role not in {'root', 'administrador'}:
        raise RuntimeError(
            "Para sincronizar 'usuarios' el rol debe ser root o administrador. "
            f"Rol actual: {role or 'desconocido'}."
        )

    if role not in {'root', 'administrador', 'distribuidor'}:
        raise RuntimeError(
            "El rol no tiene permisos para sincronizar colecciones solicitadas. "
            f"Rol actual: {role or 'desconocido'}."
        )

    return auth.get_valid_id_token(auth_session)


def main():
    args = parse_args()
    load_app_env()

    # Inicializar la base de datos y cargar todos los modelos para que 
    # SQLAlchemy configure correctamente los mappers y relaciones.
    configure_database()

    invalid = [name for name in args.collections if name not in MODEL_REGISTRY]
    if invalid:
        logger.error('Colecciones no soportadas: %s', ', '.join(invalid))
        logger.info('Colecciones permitidas: %s', ', '.join(sorted(MODEL_REGISTRY.keys())))
        return 1

    sync_manager = SyncManager()
    if not sync_manager.client.is_configured():
        logger.error('FIREBASE_DATABASE_URL no esta configurado. Revisa tu archivo .env.')
        return 1

    try:
        auth_token = _resolve_auth_token(args.collections)
        sync_manager.client.auth_token = auth_token
        logger.info('Autenticacion Firebase para bootstrap lista.')
    except Exception as exc:
        logger.error('No se pudo autenticar bootstrap: %s', exc)
        return 1

    session = SessionLocal()
    try:
        totals = {}
        for entity_name in args.collections:
            pushed_ids = sync_manager.bootstrap_collection(session, entity_name)
            totals[entity_name] = len(pushed_ids)
            logger.info('Coleccion %s sincronizada. Registros enviados: %s', entity_name, len(pushed_ids))

        logger.info('Sincronizacion inicial completada: %s', totals)
        return 0
    except Exception as exc:
        logger.error('Error en sincronizacion inicial: %s', exc)
        session.rollback()
        return 1
    finally:
        session.close()


if __name__ == '__main__':
    raise SystemExit(main())
