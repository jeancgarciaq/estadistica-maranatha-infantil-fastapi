import sqlite3
import os

db_path = r'c:\xampp\htdocs\New-Estadistica-Maranatha-Infantil-Kivy\models\app.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Base de datos no encontrada en {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Listado de tablas que utilizan AuditMixin y requieren el campo last_sync para sincronización
    # Se incluyen variaciones de nombres comunes según los modelos definidos
    tables = [
        "areas", "salones", "aulas", "donaciones", "distribuciones", 
        "logistica", "ensenanza", "otras_areas", "otrasareas", "recepciones",
        "usuarios", "roles", "permisos", "alimentos_preparados"
    ]

    try:
        for table in tables:
            # Verificar si la tabla existe en la base de datos
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                continue

            # Obtener el esquema actual de columnas
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            if 'last_sync' not in columns:
                print(f"Añadiendo columna 'last_sync' a la tabla '{table}'...")
                # SQLite no tiene tipo DATETIME nativo, SQLAlchemy lo maneja como texto
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN last_sync DATETIME")
                conn.commit()
                print(f"Columna 'last_sync' añadida exitosamente a '{table}'.")
            else:
                print(f"La columna 'last_sync' ya existe en '{table}'.")

    except Exception as e:
        print(f"Error durante la migración: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
