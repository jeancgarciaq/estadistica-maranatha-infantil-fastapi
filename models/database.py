import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Ruta de la base de datos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'app.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base declarativa para los modelos
Base = declarative_base()

# Función para crear la base de datos si no existe
def create_database():
    if not os.path.exists(DATABASE_PATH):
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