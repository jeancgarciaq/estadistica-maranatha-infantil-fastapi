import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_app_env():
    """Carga variables de entorno desde .env en la raiz del proyecto."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_candidates = [
        os.path.join(project_root, '.env')
    ]

    loaded_path = None
    for path in env_candidates:
        if os.path.exists(path):
            load_dotenv(path, override=False)
            loaded_path = path
            break

    if loaded_path:
        logger.info('Variables de entorno cargadas desde: %s', loaded_path)
    else:
        logger.info('No se encontro archivo .env ni config/firebase.env; se usan variables del sistema.')
