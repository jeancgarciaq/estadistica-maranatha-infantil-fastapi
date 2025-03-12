import logging
from models.area import Area
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ControladorArea:
    def __init__(self, vista):
        self.vista = vista

    def crear_area(self, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre del área es obligatorio.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                area = Area(nombre=nombre)
                db.add(area)
                logger.info(f"Área creada: {nombre}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear área: {e}")
            self.vista.mostrar_error("Error al crear área. Inténtalo de nuevo.")
        finally:
            self.listar_areas()

    def actualizar_area(self, id, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre del área es obligatorio.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    area.nombre = nombre
                    logger.info(f"Área actualizada: {nombre}")
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar área: {e}")
            self.vista.mostrar_error("Error al actualizar área. Inténtalo de nuevo.")
        finally:
            self.listar_areas()

    def eliminar_area(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    db.delete(area)
                    logger.info(f"Área eliminada: {area.nombre}")
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar área: {e}")
            self.vista.mostrar_error("Error al eliminar área. Inténtalo de nuevo.")
        finally:
            self.listar_areas()

    def listar_areas(self):
        db: Session = next(get_db())
        try:
            areas = db.query(Area).all()
            self.vista.actualizar_lista_areas(areas)
            logger.info("Áreas listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar áreas: {e}")
            self.vista.mostrar_error("Error al listar áreas. Inténtalo de nuevo.")

    def obtener_area(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Area).filter(Area.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener área: {e}")
            self.vista.mostrar_error("Error al obtener área. Inténtalo de nuevo.")
            return None