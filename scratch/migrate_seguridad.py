import sqlite3
import os

db_path = r'c:\xampp\htdocs\New-Estadistica-Maranatha-Infantil-Kivy\models\app.db'

if not os.path.exists(db_path):
    print(f"Base de datos no encontrada en {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar si la columna ya existe
    cursor.execute("PRAGMA table_info(otrasareas)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'seguridad' not in columns:
        print("Añadiendo columna 'seguridad' a la tabla 'otrasareas'...")
        cursor.execute("ALTER TABLE otrasareas ADD COLUMN seguridad INTEGER")
        conn.commit()
        print("Columna añadida exitosamente.")
    else:
        print("La columna 'seguridad' ya existe.")

except Exception as e:
    print(f"Error durante la migración: {e}")
finally:
    conn.close()
