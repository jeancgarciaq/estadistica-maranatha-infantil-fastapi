import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
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
    kwargs = {}
    if "sqlite" not in DATABASE_URL:
        kwargs = {
            "pool_size": 10,
            "max_overflow": 20,
            "pool_recycle": 300
        }
    engine = create_engine(
        DATABASE_URL, 
        connect_args=connect_args,
        **kwargs
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Convención de nombres para constraints (Vital para que Alembic/SQLite no se traben)
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=metadata)

def configure_database():
    """
    Sincroniza el esquema de la base de datos usando Alembic y siembra datos iniciales.
    """
    logger.info("🛠️ Iniciando configure_database...")
    from models.security import seed_security_data
    import models.security, models.donaciones, models.salones, models.aulas, models.distribucion, models.logistica, models.ensenanza, models.otras_areas, models.recepcion, models.alimento_preparado, models.alimento_preparado_componente, models.servidor, models.pastores, models.lideres, models.coordinadores, models.capitanes, models.docentes, models.auxiliares, models.colaboradores

    # Intentar ejecutar migraciones de Alembic programáticamente al iniciar la app
    try:
        ini_path = "alembic.ini"
        if not os.path.exists(ini_path):
            logger.error(f"❌ No se encontró el archivo {ini_path} en {os.getcwd()}")
            raise FileNotFoundError(f"Archivo de configuración {ini_path} no encontrado.")

        alembic_cfg = Config(ini_path)
        logger.info(f"📖 Configuración de Alembic cargada desde {ini_path}")

        # Lógica para sincronizar la base de datos sin ejecutar SQL de creación
        reset_mode = os.getenv("RESET_ALEMBIC", "false").lower() == "true"
        
        if reset_mode:
            logger.info("🔄 Modo RESET detectado. Ejecutando 'alembic stamp head'...")
            command.stamp(alembic_cfg, "head")
            logger.info("✅ Base de datos marcada como actualizada (stamp head).")
        else:
            # Aplicar todas las migraciones pendientes hasta la versión más reciente (head)
            command.upgrade(alembic_cfg, "head")
            logger.info("✅ Migraciones de Alembic aplicadas exitosamente (upgrade head).")
    except Exception as e:
        logger.warning(f"⚠️ No se pudieron aplicar las migraciones vía Alembic: {e}")
        logger.info("Intentando fallback con Base.metadata.create_all (solo creará tablas nuevas)...")
        # Fallback para garantizar que al menos las tablas existan si Alembic falla o no está configurado
        Base.metadata.create_all(bind=engine)
    
    logger.info("🌱 Iniciando siembra de datos (seeding)...")
    db = SessionLocal()
    try:
        seed_security_data(db)
        logger.info("✅ Datos de seguridad sembrados correctamente.")
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