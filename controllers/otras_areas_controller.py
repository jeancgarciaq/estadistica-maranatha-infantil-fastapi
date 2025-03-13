import logging
from models.otras_areas import OtrasAreas
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OtrasAreasController:
    def __init__(self, vista):
        self.vista = vista

    def crear_otrasareas(self, alabanza, fecha, protocolo, semillitas, sonido, teatro, tv, ujier):
        if not fecha:
            self.vista.mostrar_error("La fecha es obligatoria.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                otrasareas = OtrasAreas(alabanza=alabanza, fecha=fecha_date, protocolo=protocolo, semillitas=semillitas, sonido=sonido, teatro=teatro, tv=tv, ujier=ujier)
                db.add(otrasareas)
                logger.info(f"Otras áreas creadas: {otrasareas.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear otras áreas: {e}")
            self.vista.mostrar_error("Error al crear otras áreas. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_otrasareas()

    def actualizar_otrasareas(self, id, alabanza, fecha, protocolo, semillitas, sonido, teatro, tv, ujier):
        if not fecha:
            self.vista.mostrar_error("La fecha es obligatoria.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
                if otrasareas:
                    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                    otrasareas.alabanza = alabanza
                    otrasareas.fecha = fecha_date
                    otrasareas.protocolo = protocolo
                    otrasareas.semillitas = semillitas
                    otrasareas.sonido = sonido
                    otrasareas.teatro = teatro
                    otrasareas.tv = tv
                    otrasareas.ujier = ujier
                    logger.info(f"Otras áreas actualizadas: {otrasareas.id}")
                else:
                    self.vista.mostrar_error("Otras áreas no encontradas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar otras áreas: {e}")
            self.vista.mostrar_error("Error al actualizar otras áreas. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_otrasareas()

    def eliminar_otrasareas(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
                if otrasareas:
                    db.delete(otrasareas)
                    logger.info(f"Otras áreas eliminadas: {otrasareas.id}")
                else:
                    self.vista.mostrar_error("Otras áreas no encontradas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar otras áreas: {e}")
            self.vista.mostrar_error("Error al eliminar otras áreas. Inténtalo de nuevo.")
        finally:
            self.listar_otrasareas()

    def listar_otrasareas(self):
        db: Session = next(get_db())
        try:
            otrasareas = db.query(OtrasAreas).all()
            self.vista.actualizar_lista_otrasareas(otrasareas)
            logger.info("Otras áreas listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar otras áreas: {e}")
            self.vista.mostrar_error("Error al listar otras áreas. Inténtalo de nuevo.")

    def obtener_otrasareas(self, id):
        db: Session = next(get_db())
        try:
            return db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener otras áreas: {e}")
            self.vista.mostrar_error("Error al obtener otras áreas. Inténtalo de nuevo.")
            return None