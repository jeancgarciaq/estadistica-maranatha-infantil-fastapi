import logging
from models.ensenanza import Ensenanza
from controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnsenanzaController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Ensenanza, session=session)
        logger.info("EnsenanzaController inicializado.")

    def crear_ensenanza(self, capitan, fecha, subcapitan, user_context=None):
        """
        Crea un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        if not capitan or not fecha or not subcapitan:
            return False, "Todos los campos son obligatorios."

        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

        def operacion(db):
            ensenanza = Ensenanza(capitan=capitan, subcapitan=subcapitan, fecha=fecha_dt)
            db.add(ensenanza)
            db.flush()
            self.registrar_evento_sync(db, 'ensenanza', ensenanza, 'upsert')
            logger.info("Enseñanza creada.")

        return self.ejecutar_transaccion(operacion, "Enseñanza creada exitosamente.", user_context=user_context)

    def actualizar_ensenanza(self, id, capitan, subcapitan, fecha, user_context=None):
        """
        Actualiza un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        if not capitan or not fecha or not subcapitan:
            return False, "Todos los campos son obligatorios."

        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

        def operacion(db):
            ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id, Ensenanza.is_deleted.is_(False)).first()
            if not ensenanza:
                raise ValueError("Enseñanza no encontrada.")
            
            ensenanza.capitan = capitan
            ensenanza.subcapitan = subcapitan
            ensenanza.fecha = fecha_dt
            
            self.registrar_evento_sync(db, 'ensenanza', ensenanza, 'upsert')
            logger.info(f"Enseñanza actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Enseñanza actualizada exitosamente.", user_context=user_context)

    def eliminar_ensenanza(self, id, user_context=None):
        """
        Elimina un registro de enseñanza.
        :return: (Exito, Mensaje)
        """
        def operacion(db):
            ensenanza = db.query(Ensenanza).filter(Ensenanza.id == id, Ensenanza.is_deleted.is_(False)).first()
            if not ensenanza:
                raise ValueError("Enseñanza no encontrada.")
            
            self.marcar_eliminado(ensenanza, db)
            self.registrar_evento_sync(db, 'ensenanza', ensenanza, 'delete')
            logger.info(f"Enseñanza eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Enseñanza eliminada exitosamente.", user_context=user_context)

    def listar_ensenanzas(self, fecha=None):
        """
        Lista todos los registros de enseñanza.
        :return: Lista de objetos Ensenanza.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(Ensenanza.fecha == fecha_dt)
            
            ensenanzas = query.order_by(Ensenanza.fecha.desc()).all()
            logger.info("Enseñanzas listadas.")
            return ensenanzas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar enseñanzas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_ensenanza(self, id):
        """
        Obtiene un registro de enseñanza por ID.
        :return: Objeto Ensenanza o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Ensenanza.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener enseñanza: {e}")
            return None
        finally:
            if not self.session:
                db.close()