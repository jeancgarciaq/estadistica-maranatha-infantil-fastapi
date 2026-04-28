import os
import sys

# Añadir el directorio raíz del proyecto a la ruta de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.base import Base
from models.database import DATABASE_PATH, engine


def main():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    Base.metadata.create_all(bind=engine)
    print(f"Base de datos recreada en {DATABASE_PATH}")


if __name__ == '__main__':
    main()