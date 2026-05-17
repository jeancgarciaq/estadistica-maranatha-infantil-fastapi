import os
import sys
import logging
from sqlalchemy import text

# Añadir la raíz del proyecto al path para resolver las importaciones de models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.env_loader import load_app_env
load_app_env()

from models.database import engine, shutdown_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TruncateAlembic")

def run():
    """Conecta a Cloud SQL usando la configuración del proyecto y trunca la tabla alembic_version."""
    try:
        with engine.connect() as conn:
            logger.info("Conectando a Cloud SQL para truncar alembic_version...")
            conn.execute(text("TRUNCATE TABLE alembic_version;"))
            conn.commit()
            logger.info("✅ Tabla alembic_version truncada exitosamente.")
    except Exception as e:
        logger.error(f"❌ Error al truncar la tabla: {e}")
    finally:
        shutdown_db()

if __name__ == "__main__":
    run()