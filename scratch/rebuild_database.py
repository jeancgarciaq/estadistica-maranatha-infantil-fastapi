import os
import sys

# Añadir el directorio raíz del proyecto a la ruta de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import engine, Base, SessionLocal, configure_database, DATABASE_URL, shutdown_db
from models.security import seed_security_data

def main():
    print("--- Reconstruyendo Base de Datos ---")
    
    # Extraer la ruta del archivo si es SQLite
    if DATABASE_URL.startswith("sqlite:///"):
        db_file = DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"Archivo de base de datos eliminado: {db_file}")
            except Exception as e:
                print(f"Error al eliminar el archivo: {e}")

    # Importar todos los modelos para que Base.metadata los reconozca
    # Esto lo hace configure_database() internamente
    print("Creando tablas desde los modelos...")
    configure_database()
    
    # Sembrar datos iniciales (Roles, Permisos y Usuario Root)
    print("Sembrando datos iniciales de seguridad...")
    db = SessionLocal()
    try:
        seed_security_data(db)
        db.commit()
        print("Datos de seguridad (roles/permisos/root) creados exitosamente.")
    except Exception as e:
        db.rollback()
        print(f"Error al sembrar datos: {e}")
    finally:
        db.close()
        shutdown_db()

    print(f"Base de datos recreada y lista en: {DATABASE_URL}")


if __name__ == '__main__':
    main()