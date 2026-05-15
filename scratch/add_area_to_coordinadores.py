import os
import sys
from sqlalchemy import inspect, text

# Añadir el directorio raíz del proyecto a la ruta de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar variables de entorno (.env)
from utils.env_loader import load_app_env
load_app_env()

from models.database import engine

def migrate():
    print(f"Iniciando migración en: {engine.url}")
    
    # Usamos el inspector de SQLAlchemy para verificar columnas de forma agnóstica al motor (SQLite/Postgres)
    inspector = inspect(engine)

    try:
        # 1. Verificar si la tabla existe
        if 'coordinadores' not in inspector.get_table_names():
            print("La tabla 'coordinadores' no existe. Ejecuta primero la creación de base de datos.")
            return

        # 2. Verificar si la columna ya existe
        columns = [col['name'] for col in inspector.get_columns('coordinadores')]
        
        if 'id_area' not in columns:
            print("Añadiendo columna 'id_area' a la tabla 'coordinadores'...")
            with engine.connect() as conn:
                # SQL estándar compatible con SQLite y PostgreSQL
                conn.execute(text("ALTER TABLE coordinadores ADD COLUMN id_area INTEGER"))
                conn.commit()
            print("Columna 'id_area' añadida exitosamente.")
        else:
            print("La columna 'id_area' ya existe.")

    except Exception as e:
        print(f"Error durante la migración: {e}")

if __name__ == "__main__":
    migrate()