import os
import sys
import logging
from sqlalchemy import text

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.env_loader import load_app_env
load_app_env()

from models.database import engine, shutdown_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FixAsistenciaTable")

def run():
    """Renombra la columna id_servidor a id_persona en la base de datos Cloud SQL."""
    try:
        with engine.connect() as conn:
            logger.info("Renombrando columna 'id_servidor' a 'id_persona' en asistencia_servidores...")
            # Sintaxis de PostgreSQL para renombrar columnas
            conn.execute(text("ALTER TABLE asistencia_servidores RENAME COLUMN id_servidor TO id_persona;"))
            conn.commit()
            logger.info("✅ Columna renombrada exitosamente.")
    except Exception as e:
        logger.error(f"❌ Error al modificar la tabla: {e}")
    finally:
        shutdown_db()

if __name__ == "__main__":
    run()