import logging
from models.logistica import Logistica
from models.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogisticaController:
    def __init__(self, session=None):
        self.session = session
        logger.info("LogisticaController inicializado.")

    def get_db_session(self):
        return SessionLocal()

    def crear_logistica(self, almacen, capitan, distribucion, hidratacion, pasillo, secretaria, fecha):
        """
        Crea un registro de logística.
        :return: (Exito, Mensaje)
        """
        if not fecha:
            return False, "La fecha es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                logistica = Logistica(
                    almacen=almacen, capitan=capitan, distribucion=distribucion,
                    hidratacion=hidratacion, pasillo=pasillo, secretaria=secretaria,
                    fecha=fecha_date
                )
                db.add(logistica)
                logger.info(f"Logística creada.")
            return True, "Logística creada exitosamente."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al crear logística: {e}")
            return False, f"Error al crear logística: {e}"
        finally:
            db.close()

    def actualizar_logistica(self, id, almacen, capitan, distribucion, hidratacion, pasillo, secretaria, fecha):
        """
        Actualiza un registro de logística.
        :return: (Exito, Mensaje)
        """
        if not fecha:
            return False, "La fecha es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                logistica = db.query(Logistica).filter(Logistica.id == id).first()
                if logistica:
                    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                    logistica.almacen = almacen
                    logistica.capitan = capitan
                    logistica.distribucion = distribucion
                    logistica.hidratacion = hidratacion
                    logistica.pasillo = pasillo
                    logistica.secretaria = secretaria
                    logistica.fecha = fecha_date
                    logger.info(f"Logística actualizada: ID {id}")
                    return True, "Logística actualizada exitosamente."
                else:
                    return False, "Logística no encontrada."
        except ValueError:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar logística: {e}")
            return False, f"Error al actualizar logística: {e}"
        finally:
            db.close()

    def eliminar_logistica(self, id):
        """
        Elimina un registro de logística.
        :return: (Exito, Mensaje)
        """
        db = self.get_db_session()
        try:
            with db.begin():
                logistica = db.query(Logistica).filter(Logistica.id == id).first()
                if logistica:
                    db.delete(logistica)
                    logger.info(f"Logística eliminada: ID {id}")
                    return True, "Logística eliminada exitosamente."
                else:
                    return False, "Logística no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar logística: {e}")
            return False, f"Error al eliminar logística: {e}"
        finally:
            db.close()

    def listar_logisticas(self):
        """
        Lista todos los registros de logística.
        :return: Lista de objetos Logistica.
        """
        db = self.get_db_session()
        try:
            logisticas = db.query(Logistica).all()
            logger.info("Logísticas listadas.")
            return logisticas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar logísticas: {e}")
            return []
        finally:
            db.close()

    def obtener_logistica(self, id):
        """
        Obtiene un registro de logística por ID.
        :return: Objeto Logistica o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Logistica).filter(Logistica.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener logística: {e}")
            return None
        finally:
            db.close()