import os
import sys
import logging
from sqlalchemy import text

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar variables de entorno antes de importar modelos que dependan de ellas
from utils.env_loader import load_app_env
load_app_env()

from models.database import engine, SessionLocal, configure_database, shutdown_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CloudSQLTest")

def test_connection():
    instancia = os.getenv("INSTANCE_CONNECTION_NAME")
    db_name = os.getenv("DB_NAME")
    ip_mode = "PRIVADA" if os.getenv("PRIVATE_IP") else "PÚBLICA"

    if not instancia:
        logger.error("INSTANCE_CONNECTION_NAME no configurada en el .env")
        return

    logger.info(f"Conectando a Cloud SQL vía Python Connector...")
    logger.info(f"Instancia: {instancia}")
    logger.info(f"Base de datos: {db_name}")
    logger.info(f"Tipo de IP: {ip_mode}")
    logger.info("Usando Application Default Credentials (ADC)")

    try:
        # 1. Prueba de conexión básica y versión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()
            logger.info(f"✅ Conexión exitosa!")
            logger.info(f"Versión de DB: {version[0]}")

        # 2. Prueba de inicialización de tablas (Opcional)
        print("\n¿Deseas intentar crear las tablas y sembrar datos iniciales? (s/n): ", end="")
        choice = input().lower()
        
        if choice == 's':
            logger.info("Configurando tablas y datos de seguridad...")
            configure_database()
            logger.info("✅ Tablas e índices creados/verificados correctamente.")
            
            # Verificar si se puede consultar la tabla de usuarios
            db = SessionLocal()
            from models.security import Usuario
            count = db.query(Usuario).count()
            logger.info(f"Usuarios en la base de datos: {count}")
            db.close()
        else:
            logger.info("Operación de creación de tablas omitida.")

        print("\n=== Prueba completada con éxito ===")

    except Exception as e:
        logger.error(f"❌ Fallo al conectar a Cloud SQL: {e}")
    
    finally:
        shutdown_db()

if __name__ == "__main__":
    test_connection()