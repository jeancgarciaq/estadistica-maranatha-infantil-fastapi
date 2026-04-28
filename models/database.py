import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

# Ruta de la base de datos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'app.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

# Función para crear la base de datos si no existe
def create_database():
    if not os.path.exists(DATABASE_PATH):
        Base.metadata.create_all(bind=engine)


def reset_database():
    """Elimina la base local y la recrea desde el esquema actual."""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    Base.metadata.create_all(bind=engine)

# Llama a la función para crear la base de datos
create_database()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()