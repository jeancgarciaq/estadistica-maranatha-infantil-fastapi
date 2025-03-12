import logging
from models.donaciones import Donacion
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ControladorDonacion:
    def __init__(self, vista):
        self.vista = vista

    def crear_donacion(self, cantidad, descripcion, equipo, fecha, sembrador, salones_ids):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Creación de donación)
                logger.info(f"Donación creada: {donacion.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear donación: {e}")
            self.vista.mostrar_error("Error al crear donación. Inténtalo de nuevo.")
        finally:
            self.listar_donaciones()

    def actualizar_donacion(self, id, cantidad, descripcion, equipo, fecha, sembrador, salones_ids):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Actualización de donación)
                logger.info(f"Donación actualizada: {donacion.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar donación: {e}")
            self.vista.mostrar_error("Error al actualizar donación. Inténtalo de nuevo.")
        finally:
            self.listar_donaciones()

    def eliminar_donacion(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Eliminación de donación)
                logger.info(f"Donación eliminada: {donacion.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar donación: {e}")
            self.vista.mostrar_error("Error al eliminar donación. Inténtalo de nuevo.")
        finally:
            self.listar_donaciones()

    def listar_donaciones(self):
        db: Session = next(get_db())
        try:
            donaciones = db.query(Donacion).all()
            self.vista.actualizar_lista_donaciones(donaciones)
            logger.info("Donaciones listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            self.vista.mostrar_error("Error al listar donaciones. Inténtalo de nuevo.")

    def obtener_donacion(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Donacion).filter(Donacion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener donación: {e}")
            self.vista.mostrar_error("Error al obtener donación. Inténtalo de nuevo.")
            return None