import os
import sys
from logging.config import fileConfig

# 1. Añadimos la raíz del proyecto al path inmediatamente
sys.path.append(os.getcwd())

# 2. Cargar variables de entorno ANTES de importar modelos o base de datos
from utils.env_loader import load_app_env
load_app_env()

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from models.database import Base
# Es CRUCIAL importar todos los modelos para que Base.metadata los reconozca
import models

config = context.config

# Interpretamos el archivo de config para el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definimos el target_metadata para que autogenerate funcione
target_metadata = Base.metadata

def get_url():
    url = os.getenv("DATABASE_URL", "sqlite:///./models/app.db")
    # Asegurar compatibilidad con SQLAlchemy 2.0 y forzar el driver pg8000
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+pg8000://", 1)
    elif url.startswith("postgresql"):
        # Si ya tiene un driver (como +psycopg2) o no tiene ninguno, forzamos +pg8000
        if "://" in url:
            prefix = url.split("://")[0]
            if prefix != "postgresql+pg8000":
                url = url.replace(prefix, "postgresql+pg8000", 1)
    return url


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "pyformat"},
        render_as_batch=True,
        # Permite detectar cambios en tipos de datos al autogenerar localmente
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
    instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")

    if instance_connection_name:
        # Si detectamos la instancia de Cloud SQL, usamos el conector que ya instalaste
        from models.database import getconn
        connectable = create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            poolclass=pool.NullPool,
        )
    else:
        # Si no, usamos la URL estándar (para SQLite o Postgres local)
        configuration = config.get_section(config.config_ini_section, {})
        configuration["sqlalchemy.url"] = get_url()
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Esto permite detectar cambios en tipos de columnas y campos nuevos
            compare_type=True,
            # Detectar cambios en valores por defecto (server_default)
            compare_server_default=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
