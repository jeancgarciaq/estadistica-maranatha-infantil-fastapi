import logging
from models.ensenanza import Ensenanza
from models.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnsenanzaController:
    def __init__(self, session=None):
        self.session = session
        logger.info("EnsenanzaController inicializado.")

    def get_db_session(self):
        return SessionLocal()

    def crear_ensenanza(self, capitan, fecha, subcapitan):
        """
        Crea un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        if not capitan or not fecha or not subcapitan:
            return False, "Todos los campos son obligatorios."

        db = self.get_db_session()
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                ensenanza = Ensenanza(capitan=capitan, subcapitan=subcapitan, fecha=fecha_date)
                db.add(ensenanza)
                logger.info(f"Enseñanza creada.")
            return True, "Enseñanza creada exitosamente."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al crear enseñanza: {e}")
            return False, f"Error al crear enseñanza: {e}"
        finally:
            db.close()

    def actualizar_ensenanza(self, id, capitan, subcapitan, fecha):
        """
        Actualiza un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        if not capitan or not fecha or not subcapitan:
            return False, "Todos los campos son obligatorios."

        db = self.get_db_session()
        try:
            with db.begin():
                ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id).first()
                if ensenanza:
                    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                    ensenanza.capitan = capitan
                    ensenanza.subcapitan = subcapitan
                    ensenanza.fecha = fecha_date
                    logger.info(f"Enseñanza actualizada: ID {id}")
                    return True, "Enseñanza actualizada exitosamente."
                else:
                    return False, "Enseñanza no encontrada."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar enseñanza: {e}")
            return False, f"Error al actualizar enseñanza: {e}"
        finally:
            db.close()

    def eliminar_ensenanza(self, id):
        """
        Elimina un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        db = self.get_db_session()
        try:
            with db.begin():
                ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id).first()
                if ensenanza:
                    db.delete(ensenanza)
                    logger.info(f"Enseñanza eliminada: ID {id}")
                    return True, "Enseñanza eliminada exitosamente."
                else:
                    return False, "Enseñanza no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar enseñanza: {e}")
            return False, f"Error al eliminar enseñanza: {e}"
        finally:
            db.close()

    def listar_ensenanzas(self):
        """
        Lista todos los registros de enseñanza.
        :return: Lista de objetos Ensenanza.
        """
        db = self.get_db_session()
        try:
            ensenanzas = db.query(Ensenanza).all()
            logger.info("Enseñanzas listadas.")
            return ensenanzas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar enseñanzas: {e}")
            return []
        finally:
            db.close()

    def obtener_ensenanza(self, id):
        """
        Obtiene un registro de enseñanza por ID.
        :return: Objeto Ensenanza o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Ensenanza).filter(Ensenanza.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener enseñanza: {e}")
            return None
        finally:
            db.close()