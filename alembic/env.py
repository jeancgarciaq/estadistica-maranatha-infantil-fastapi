from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from kivy.app import App
from alembic import context

import os
import sys
from logging.config import fileConfig

#Base implementación alembic
sys.path.append(os.getcwd())
from models.base import Base
import models.areas
import models.salones
import models.aulas
import models.donaciones
import models.distribucion
import models.ensenanza
import models.logistica
import models.otras_areas
import models.recepcion
import models.security


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Ajustar URL para Android si es necesario
    url = None
    try:
        from kivy.utils import platform
        if platform == 'android':
            db_path = os.path.join(App.get_running_app().user_data_dir, 'app.db')
            url = f"sqlite:///{db_path}"
    except Exception:
        url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run the migrations in a 'live' database environment.

    Rather than running the migrations across an already live
    database, first create a transaction and within that
    transaction run the migrations.
    """
    section = config.get_section(config.config_ini_section)
    
    # Ajustar URL dinámicamente para el entorno Android
    try:
        from kivy.utils import platform
        if platform == 'android':
            db_path = os.path.join(App.get_running_app().user_data_dir, 'app.db')
            section['sqlalchemy.url'] = f"sqlite:///{db_path}"
    except Exception:
        pass

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
