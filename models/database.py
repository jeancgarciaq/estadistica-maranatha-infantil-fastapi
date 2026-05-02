import os

try:
    from kivy.app import App
except ImportError:
    App = None

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

_engine = None
_session_factory = None
_database_path = None


def _resolve_database_path():
    database_path = os.environ.get('APP_DB_PATH')
    if database_path:
        return database_path

    try:
        app = App.get_running_app()
    except Exception:
        app = None

    if app and getattr(app, 'user_data_dir', None):
        return os.path.join(app.user_data_dir, 'app.db')

    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')


def configure_database(database_path=None):
    global _engine, _session_factory, _database_path

    resolved_path = database_path or _resolve_database_path()
    if _session_factory is not None and resolved_path == _database_path:
        return _session_factory

    os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
    _engine = create_engine(f'sqlite:///{resolved_path}')
    _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    _database_path = resolved_path

    Base.metadata.create_all(bind=_engine)
    return _session_factory


def SessionLocal():
    return configure_database()()

#Modelos
from models.areas import Area
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.salones import Salon
from models.aulas import Aula
from models.donaciones import Donacion
from models.distribucion import Distribucion
from models.ensenanza import Ensenanza
from models.logistica import Logistica
from models.otras_areas import OtrasAreas
from models.recepcion import Recepcion
from models.sync_queue import SyncQueue
from models.security import Usuario, Rol, Permiso

def create_database():
    configure_database()


def reset_database():
    """Elimina la base local y la recrea desde el esquema actual."""
    database_path = _resolve_database_path()
    if os.path.exists(database_path):
        os.remove(database_path)
    configure_database(database_path)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()