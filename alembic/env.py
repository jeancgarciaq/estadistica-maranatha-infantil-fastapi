import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Añadimos la raíz del proyecto al path para poder importar los modelos
sys.path.append(os.getcwd())

# Importamos la configuración del entorno y la Base de datos
from utils.env_loader import load_app_env
from models.database import Base
# Es CRUCIAL importar todos los modelos para que Base.metadata los reconozca
import models.security, models.donaciones, models.salones, models.aulas
import models.distribucion, models.logistica, models.ensenanza
import models.otras_areas, models.recepcion, models.alimento_preparado

load_app_env()

# este es el objeto config de Alembic
config = context.config

# Interpretamos el archivo de config para el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definimos el target_metadata para que autogenerate funcione
target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "sqlite:///./models/app.db")

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "pyformat"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
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
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
