import os
import time
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from alembic import command
from alembic.config import Config

# Lazy import del conector de Google Cloud SQL (solo si se usa)
_connector = None

def _get_connector():
    global _connector
    if _connector is None:
        from google.cloud.sql.connector import Connector
        _connector = Connector(refresh_strategy="LAZY")
    return _connector

# Configuración desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

logger = logging.getLogger(__name__)

def getconn():
    """Conexión via Google Cloud SQL Connector (solo si INSTANCE_CONNECTION_NAME está definido)."""
    connector = _get_connector()
    db_user = os.getenv("DB_USER", "").strip()
    db_pass = os.getenv("DB_PASS", "").strip()
    db_name = os.getenv("DB_NAME", "").strip()
    private_ip = os.getenv("PRIVATE_IP", "").strip().lower()
    
    from google.cloud.sql.connector import IPTypes
    ip_type = IPTypes.PRIVATE if private_ip == "true" else IPTypes.PUBLIC

    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=ip_type
    )

def shutdown_db():
    """Cierra el conector de Cloud SQL si fue inicializado."""
    global _connector
    if _connector is not None:
        try:
            _connector.close()
        except Exception:
            pass
        _connector = None

# Normalizar DATABASE_URL
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./models/app.db"
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)
    elif DATABASE_URL.startswith("postgresql"):
        if "://" in DATABASE_URL:
            prefix = DATABASE_URL.split("://")[0]
            if prefix != "postgresql+pg8000":
                DATABASE_URL = DATABASE_URL.replace(prefix, "postgresql+pg8000", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# Crear engine según configuración
if INSTANCE_CONNECTION_NAME:
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=10,
        max_overflow=20,
        pool_recycle=300
    )
else:
    kwargs = {}
    if "sqlite" not in DATABASE_URL:
        kwargs = {
            "pool_size": 10,
            "max_overflow": 20,
            "pool_recycle": 300
        }
    engine = create_engine(DATABASE_URL, connect_args=connect_args, **kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata con naming convention para Alembic/SQLite
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=metadata)

def configure_database():
    logger.info("🛠️ Iniciando configure_database...")
    start_time = time.time()
    from models.security import seed_security_data
    import models.security, models.areas, models.donaciones, models.salones, models.aulas, models.distribucion, models.logistica, models.ensenanza, models.otras_areas, models.recepcion, models.alimento_preparado, models.alimento_preparado_componente, models.pastores, models.lideres, models.coordinadores, models.capitanes, models.docentes, models.auxiliares, models.colaboradores, models.servidor

    engine.dispose()
    
    if "sqlite" in DATABASE_URL:
        logger.info("🧪 Modo SQLite detectado: creando tablas con Base.metadata.create_all")
        Base.metadata.create_all(bind=engine)
    else:
        try:
            ini_path = "alembic.ini"
            if not os.path.exists(ini_path):
                logger.error(f"❌ No se encontró el archivo {ini_path} en {os.getcwd()}")
                raise FileNotFoundError(f"Archivo de configuración {ini_path} no encontrado.")
            
            alembic_cfg = Config(ini_path)
            logger.info(f"📖 Configuración de Alembic cargada desde {ini_path}")
            
            reset_mode = os.getenv("RESET_ALEMBIC", "false").lower() == "true"
            if reset_mode:
                logger.info("🔄 Modo RESET detectado. Ejecutando 'alembic stamp head'...")
                command.stamp(alembic_cfg, "head")
                logger.info("✅ Base de datos marcada como actualizada (stamp head).")
            else:
                logger.info("🧩 Ejecutando migraciones de Alembic hasta head...")
                command.upgrade(alembic_cfg, "head")
                logger.info("✅ Migraciones de Alembic aplicadas exitosamente (upgrade head) en %.2fs.", time.time() - start_time)
        except Exception as e:
            logger.warning(f"⚠️ No se pudieron aplicar las migraciones vía Alembic: {e}")
            logger.info("Intentando fallback con Base.metadata.create_all...")
            Base.metadata.create_all(bind=engine)
    
    logger.info("🌱 Iniciando siembra de datos (seeding)...")
    db = SessionLocal()
    try:
        seed_security_data(db)
        logger.info("✅ Datos de seguridad sembrados correctamente en %.2fs.", time.time() - start_time)
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()