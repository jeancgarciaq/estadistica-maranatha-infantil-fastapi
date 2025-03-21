import logging
from models.ensenanza import Ensenanza
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnsenanzaController:
    def __init__(self, vista):
        self.vista = vista

    def crear_ensenanza(self, capitan, fecha, subcapitan):
        if not capitan or not fecha or not subcapitan:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                ensenanza = Ensenanza(capitan=capitan, subcapitan=subcapitan, fecha=fecha_date)
                db.add(ensenanza)
                logger.info(f"Enseñanza creada: {ensenanza.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear enseñanza: {e}")
            self.vista.mostrar_error("Error al crear enseñanza. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_ensenanzas()

    def actualizar_ensenanza(self, id, capitan, subcapitan, fecha):
        if not capitan or not fecha or not subcapitan:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id).first()
                if ensenanza:
                    fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                    ensenanza.capitan = capitan
                    ensenanza.subcapitan = subcapitan
                    ensenanza.fecha = fecha_date
                    logger.info(f"Enseñanza actualizada: {ensenanza.id}")
                else:
                    self.vista.mostrar_error("Enseñanza no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar enseñanza: {e}")
            self.vista.mostrar_error("Error al actualizar enseñanza. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_ensenanzas()

    def eliminar_ensenanza(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id).first()
                if ensenanza:
                    db.delete(ensenanza)
                    logger.info(f"Enseñanza eliminada: {ensenanza.id}")
                else:
                    self.vista.mostrar_error("Enseñanza no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar enseñanza: {e}")
            self.vista.mostrar_error("Error al eliminar enseñanza. Inténtalo de nuevo.")
        finally:
            self.listar_ensenanzas()

    def listar_ensenanzas(self):
        db: Session = next(get_db())
        try:
            ensenanzas = db.query(Ensenanza).all()
            self.vista.actualizar_lista_ensenanzas(ensenanzas)
            logger.info("Enseñanzas listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar enseñanzas: {e}")
            self.vista.mostrar_error("Error al listar enseñanzas. Inténtalo de nuevo.")

    def obtener_ensenanza(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Ensenanza).filter(Ensenanza.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener enseñanza: {e}")
            self.vista.mostrar_error("Error al obtener enseñanza. Inténtalo de nuevo.")
            return None