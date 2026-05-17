import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
import logging
from alembic import command
from alembic.config import Config

# En la web, usamos una ruta relativa o absoluta definida en el entorno
# Si estamos en local usa SQLite, si estamos en la nube usará el string de PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME") # e.g. project:region:instance

# Inicializar el conector de Google Cloud SQL
connector = Connector(refresh_strategy="LAZY")

logger = logging.getLogger(__name__)

def getconn():
    """Función para que SQLAlchemy obtenga conexiones a través del conector de Google."""
    # Usamos .strip() para eliminar espacios en blanco o saltos de línea accidentales del .env
    db_user = os.getenv("DB_USER", "").strip()
    db_pass = os.getenv("DB_PASS", "").strip()
    db_name = os.getenv("DB_NAME", "").strip()
    
    private_ip = os.getenv("PRIVATE_IP", "").strip().lower()
    ip_type = IPTypes.PRIVATE if private_ip == "true" else IPTypes.PUBLIC

    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=ip_type
    )
    return conn

def shutdown_db():
    """
    Cierra el conector de Cloud SQL. 
    Debe llamarse al apagar la aplicación FastAPI.
    """
    if connector:
        try:
            connector.close()
        except Exception:
            pass

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./models/app.db"
else:
    # Asegurar compatibilidad con SQLAlchemy 2.0 y forzar el driver pg8000
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)
    elif DATABASE_URL.startswith("postgresql"):
        # Si ya tiene un driver (como +psycopg2) o no tiene ninguno, forzamos +pg8000
        if "://" in DATABASE_URL:
            prefix = DATABASE_URL.split("://")[0]
            if prefix != "postgresql+pg8000":
                DATABASE_URL = DATABASE_URL.replace(prefix, "postgresql+pg8000", 1)

# Argumentos de conexión específicos por motor
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

if INSTANCE_CONNECTION_NAME:
    # Si tenemos el nombre de instancia, usamos el conector oficial
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=10,
        max_overflow=20,
        pool_recycle=300
    )
else:
    # Fallback a URL estándar (SQLite o Postgres TCP)
    engine = create_engine(
        DATABASE_URL, 
        connect_args=connect_args,
        pool_size=10,
        max_overflow=20,
        pool_recycle=300
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def configure_database():
    """
    Sincroniza el esquema de la base de datos usando Alembic y siembra datos iniciales.
    """
    from models.security import seed_security_data
    import models.security, models.donaciones, models.salones, models.aulas, models.distribucion, models.logistica, models.ensenanza, models.otras_areas, models.recepcion, models.alimento_preparado, models.alimento_preparado_componente, models.servidor, models.pastores, models.lideres, models.coordinadores, models.capitanes, models.docentes, models.auxiliares, models.colaboradores

    # Intentar ejecutar migraciones de Alembic programáticamente al iniciar la app
    try:
        # Se asume que alembic.ini está en la raíz del proyecto
        alembic_cfg = Config("alembic.ini")
        # Aplicar todas las migraciones pendientes hasta la versión más reciente (head)
        command.upgrade(alembic_cfg, "head")
        logger.info("✅ Migraciones de Alembic aplicadas exitosamente (upgrade head).")
    except Exception as e:
        logger.warning(f"⚠️ No se pudieron aplicar las migraciones vía Alembic: {e}")
        logger.info("Intentando fallback con Base.metadata.create_all (solo creará tablas nuevas)...")
        # Fallback para garantizar que al menos las tablas existan si Alembic falla o no está configurado
        Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_security_data(db)
    finally:
        db.close()

def get_db():
    """
    Generador de sesiones para FastAPI (Dependency Injection).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()