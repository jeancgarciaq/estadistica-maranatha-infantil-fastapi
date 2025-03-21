import logging
from models.logistica import Logistica
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogisticaController:
    def __init__(self, vista):
        self.vista = vista

    def crear_logistica(self, almacen, capitan, distribucion, hidratacion, pasillo, secretaria, fecha):
        if not fecha:
            self.vista.mostrar_error("La fecha es obligatoria.")
            return

        db: Session = next(get_db())
        try:
            with db.begin():
                fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
                logistica = Logistica(almacen=almacen, capitan=capitan, distribucion=distribucion, hidratacion=hidratacion, pasillo=pasillo, secretaria=secretaria, fecha=fecha_date)
                db.add(logistica)
                logger.info(f"Logística creada: {logistica.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear logística: {e}")
            self.vista.mostrar_error("Error al crear logística. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_logisticas()

    def actualizar_logistica(self, id, almacen, capitan, distribucion, hidratacion, pasillo, secretaria, fecha):
        if not fecha:
            self.vista.mostrar_error("La fecha es obligatoria.")
            return

        db: Session = next(get_db())
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
                    logger.info(f"Logística actualizada: {logistica.id}")
                else:
                    self.vista.mostrar_error("Logística no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar logística: {e}")
            self.vista.mostrar_error("Error al actualizar logística. Inténtalo de nuevo.")
        except ValueError as e:
            logger.error(f"Error de formato de fecha: {e}")
            self.vista.mostrar_error("Error: Formato de fecha incorrecto (YYYY-MM-DD).")
        finally:
            self.listar_logisticas()

    def eliminar_logistica(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                logistica = db.query(Logistica).filter(Logistica.id == id).first()
                if logistica:
                    db.delete(logistica)
                    logger.info(f"Logística eliminada: {logistica.id}")
                else:
                    self.vista.mostrar_error("Logística no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar logística: {e}")
            self.vista.mostrar_error("Error al eliminar logística. Inténtalo de nuevo.")
        finally:
            self.listar_logisticas()

    def listar_logisticas(self):
        db: Session = next(get_db())
        try:
            logisticas = db.query(Logistica).all()
            self.vista.actualizar_lista_logisticas(logisticas)
            logger.info("Logísticas listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar logísticas: {e}")
            self.vista.mostrar_error("Error al listar logísticas. Inténtalo de nuevo.")

    def obtener_logistica(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Logistica).filter(Logistica.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener logística: {e}")
            self.vista.mostrar_error("Error al obtener logística. Inténtalo de nuevo.")
            return None