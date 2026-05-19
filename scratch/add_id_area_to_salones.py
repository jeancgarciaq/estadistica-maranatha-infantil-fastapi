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
logger = logging.getLogger("AddColumnSalones")

def run():
    """Conecta a Cloud SQL y añade manualmente la columna id_area a la tabla salones."""
    try:
        with engine.connect() as conn:
            logger.info("Conectando a Cloud SQL para modificar la tabla 'salones'...")
            
            # 1. Añadir la columna
            # Nota: id_area debe ser INTEGER para coincidir con areas.id
            logger.info("Añadiendo columna 'id_area'...")
            conn.execute(text("ALTER TABLE salones ADD COLUMN id_area INTEGER;"))
            
            # 2. Añadir la Foreign Key
            logger.info("Añadiendo restricción de llave foránea...")
            conn.execute(text("""
                ALTER TABLE salones 
                ADD CONSTRAINT fk_salones_id_area_areas 
                FOREIGN KEY (id_area) REFERENCES areas (id) 
                ON DELETE SET NULL;
            """))
            
            conn.commit()
            logger.info("✅ Columna y restricción añadidas exitosamente.")
    except Exception as e:
        logger.error(f"❌ Error al modificar la tabla: {e}")
    finally:
        shutdown_db()

if __name__ == "__main__":
    run()