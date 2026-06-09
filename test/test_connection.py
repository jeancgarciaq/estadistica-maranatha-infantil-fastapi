import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

#variables de conexión postgresql
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 1. Construye la URL de conexión (Dialecto async o sync, usaremos sync para la prueba)
DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Crea el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

print("🔄 Intentando conectar a Cloud SQL a través del Proxy...")

try:
    # 3. Abrir la conexión y ejecutar un SELECT simple
    with engine.connect() as conexion:
        # Reemplaza 'tu_tabla' por el nombre real de una entidad que ya tenga datos
        # Usamos text() para declarar la consulta SQL pura de forma segura
        query = text("SELECT * FROM capitanes LIMIT 5;") 
        
        resultado = conexion.execute(query)
        
        print("\n✅ ¡Conexión exitosa! Mostrando los primeros registros:\n")
        
        # 4. Iterar y pintar los resultados en consola
        for fila in resultado:
            print(fila)
            
except OperationalError as e:
    print("\n❌ Error de conexión. Revisa lo siguiente:")
    print("- ¿El Cloud SQL Auth Proxy está corriendo en otra terminal?")
    print("- ¿El usuario, contraseña o nombre de la base de datos son correctos?")
    print(f"\nDetalle del error:\n{e}")