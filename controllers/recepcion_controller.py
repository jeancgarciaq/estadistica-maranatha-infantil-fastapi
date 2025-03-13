import logging
from models.recepcion import Recepcion
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecepcionController:
    def __init__(self, vista):
        self.vista = vista

    def crear_recepcion(self, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre es obligatorio.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                recepcion = Recepcion(nombre=nombre)
                db.add(recepcion)
                logger.info(f"Recepción creada: {recepcion.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear recepción: {e}")
            self.vista.mostrar_error("Error al crear recepción. Inténtalo de nuevo.")
        finally:
            self.listar_recepciones()

    def actualizar_recepcion(self, id, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre es obligatorio.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                recepcion = db.query(Recepcion).filter(Recepcion.id == id).first()
                if recepcion:
                    recepcion.nombre = nombre
                    logger.info(f"Recepción actualizada: {recepcion.id}")
                else:
                    self.vista.mostrar_error("Recepción no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar recepción: {e}")
            self.vista.mostrar_error("Error al actualizar recepción. Inténtalo de nuevo.")
        finally:
            self.listar_recepciones()

    def eliminar_recepcion(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                recepcion = db.query(Recepcion).filter(Recepcion.id == id).first()
                if recepcion:
                    db.delete(recepcion)
                    logger.info(f"Recepción eliminada: {recepcion.id}")
                else:
                    self.vista.mostrar_error("Recepción no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar recepción: {e}")
            self.vista.mostrar_error("Error al eliminar recepción. Inténtalo de nuevo.")
        finally:
            self.listar_recepciones()

    def listar_recepciones(self):
        db: Session = next(get_db())
        try:
            recepciones = db.query(Recepcion).all()
            self.vista.actualizar_lista_recepciones(recepciones)
            logger.info("Recepciones listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar recepciones: {e}")
            self.vista.mostrar_error("Error al listar recepciones. Inténtalo de nuevo.")

    def obtener_recepcion(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Recepcion).filter(Recepcion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener recepción: {e}")
            self.vista.mostrar_error("Error al obtener recepción. Inténtalo de nuevo.")
            return None