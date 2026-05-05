import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# En la web, usamos una ruta relativa o absoluta definida en el entorno
# Si estamos en local usa SQLite, si estamos en la nube usará el string de PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./models/app.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def configure_database():
    """
    Crea las tablas si no existen. 
    Nota: En producción es mejor usar Alembic, pero esto asegura que la app corra.
    """
    from models.security import seed_security_data
    import models.security, models.donaciones, models.salones, models.aulas, models.distribucion, models.logistica, models.ensenanza, models.otras_areas, models.recepcion, models.alimento_preparado, models.alimento_preparado_componente
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