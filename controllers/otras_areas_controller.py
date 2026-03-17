import logging
from models.otras_areas import OtrasAreas
from models.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OtrasAreasController:
    def __init__(self, session=None):
        self.session = session
        logger.info("OtrasAreasController inicializado.")

    def get_db_session(self):
        return SessionLocal()

    def crear_otrasareas(self, alabanza, protocolo, semillitas, sonido, teatro, tv, ujier, fecha):
        """
        Crea un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        if not fecha:
            return False, "La fecha es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                otrasareas = OtrasAreas(
                    alabanza=alabanza, protocolo=protocolo, semillitas=semillitas,
                    sonido=sonido, teatro=teatro, tv=tv, ujier=ujier, fecha=fecha_date
                )
                db.add(otrasareas)
                logger.info(f"Otras áreas creadas.")
            return True, "Otras áreas creadas exitosamente."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al crear otras áreas: {e}")
            return False, f"Error al crear otras áreas: {e}"
        finally:
            db.close()

    def actualizar_otrasareas(self, id, alabanza, protocolo, semillitas, sonido, teatro, tv, ujier, fecha):
        """
        Actualiza un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        if not fecha:
            return False, "La fecha es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
                if otrasareas:
                    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                    otrasareas.alabanza = alabanza
                    otrasareas.protocolo = protocolo
                    otrasareas.semillitas = semillitas
                    otrasareas.sonido = sonido
                    otrasareas.teatro = teatro
                    otrasareas.tv = tv
                    otrasareas.ujier = ujier
                    otrasareas.fecha = fecha_date
                    logger.info(f"Otras áreas actualizadas: ID {id}")
                    return True, "Otras áreas actualizadas exitosamente."
                else:
                    return False, "Otras áreas no encontradas."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar otras áreas: {e}")
            return False, f"Error al actualizar otras áreas: {e}"
        finally:
            db.close()

    def eliminar_otrasareas(self, id):
        """
        Elimina un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        db = self.get_db_session()
        try:
            with db.begin():
                otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
                if otrasareas:
                    db.delete(otrasareas)
                    logger.info(f"Otras áreas eliminadas: ID {id}")
                    return True, "Otras áreas eliminadas exitosamente."
                else:
                    return False, "Otras áreas no encontradas."
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar otras áreas: {e}")
            return False, f"Error al eliminar otras áreas: {e}"
        finally:
            db.close()

    def listar_otrasareas(self):
        """
        Lista todos los registros de otras áreas.
        :return: Lista de objetos OtrasAreas.
        """
        db = self.get_db_session()
        try:
            otrasareas = db.query(OtrasAreas).all()
            logger.info("Otras áreas listadas.")
            return otrasareas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar otras áreas: {e}")
            return []
        finally:
            db.close()

    def obtener_otrasareas(self, id):
        """
        Obtiene un registro de otras áreas por ID.
        :return: Objeto OtrasAreas o None.
        """
        db = self.get_db_session()
        try:
            return db.query(OtrasAreas).filter(OtrasAreas.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener otras áreas: {e}")
            return None
        finally:
            db.close()