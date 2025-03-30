import logging
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonesController:
    def __init__(self, vista):
        self.vista = vista

    def crear_salon(self, salon, edad):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Creación de salón)
                logger.info(f"Salón creado: {salon.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear salón: {e}")
            self.vista.mostrar_error("Error al crear salón. Inténtalo de nuevo.")
        finally:
            self.listar_salones()

    def actualizar_salon(self, id, salon, edad):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Actualización de salón)
                logger.info(f"Salón actualizado: {salon.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar salón: {e}")
            self.vista.mostrar_error("Error al actualizar salón. Inténtalo de nuevo.")
        finally:
            self.listar_salones()

    def eliminar_salon(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Eliminación de salón)
                logger.info(f"Salón eliminado: {salon.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar salón: {e}")
            self.vista.mostrar_error("Error al eliminar salón. Inténtalo de nuevo.")
        finally:
            self.listar_salones()

    def listar_salones(self):
        db: Session = next(get_db())
        try:
            salones = db.query(Salon).all()
            self.vista.actualizar_lista_salones(salones)
            logger.info("Salones listados.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones: {e}")
            self.vista.mostrar_error("Error al listar salones. Inténtalo de nuevo.")

    def obtener_todos_los_salones(self):
        db: Session = next(get_db())
        try:
            salones = db.query(Salon).all()
            logger.info("Todos los salones obtenidos.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salones: {e}")
            return []

    def mostrar_lista_salones(self):
        try:
            self.vista.current = "lista_salones"
            logger.info("Ventana de lista de salones desplegada.")
        except Exception as e:
            logger.error(f"Error al mostrar la ventana de lista de salones: {e}")
            self.vista.mostrar_error("Error al mostrar la lista de salones. Inténtalo de nuevo.")