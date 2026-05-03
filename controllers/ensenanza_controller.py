from controllers.base_controller import BaseController
from models.ensenanza import Ensenanza
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnsenanzaController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Ensenanza, session=session)
        logger.info("EnsenanzaController inicializado.")

    def crear_ensenanza(self, capitan, fecha, subcapitan, user_context=None):
        if not capitan or not fecha or subcapitan is None:
            return False, "Todos los campos son obligatorios."

        fecha_obj = self.validar_y_convertir_fecha(fecha)
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            reg = Ensenanza(capitan=capitan, fecha=fecha_obj, subcapitan=int(subcapitan))
            db.add(reg)
            db.flush()
            self.registrar_evento_sync(db, 'ensenanza', reg, 'upsert')
            logger.info(f"Registro de enseñanza creado: {capitan}")

        return self.ejecutar_transaccion(operacion, "Enseñanza registrada exitosamente.", user_context=user_context)

    def actualizar_ensenanza(self, id, capitan, subcapitan, fecha, user_context=None):
        if not id or not capitan or not fecha or subcapitan is None:
            return False, "Todos los campos son obligatorios."

        fecha_obj = self.validar_y_convertir_fecha(fecha)
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            reg = self.query_activa(db).filter(Ensenanza.id == id).first()
            if not reg:
                raise ValueError("Registro de enseñanza no encontrado.")
            
            reg.capitan = capitan
            reg.subcapitan = int(subcapitan)
            reg.fecha = fecha_obj
            self.registrar_evento_sync(db, 'ensenanza', reg, 'upsert')
            logger.info(f"Enseñanza actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Enseñanza actualizada exitosamente.", user_context=user_context)
                
    def eliminar_ensenanza(self, id, user_context=None):
        if not id:
            return False, "El ID es obligatorio."

        def operacion(db):
            reg = self.query_activa(db).filter(Ensenanza.id == id).first()
            if not reg:
                raise ValueError("Registro no encontrado.")
            
            self.marcar_eliminado(reg, db)
            self.registrar_evento_sync(db, 'ensenanza', reg, 'delete')
            logger.info(f"Enseñanza eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Registro eliminado exitosamente.", user_context=user_context)

    def listar_ensenanzas(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Ensenanza.fecha.desc(), Ensenanza.id.desc()).all()
        finally:
            if not self.session:
                db.close()

    def obtener_ensenanza(self, id):
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Ensenanza.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener enseñanza: {e}")
            return None
        finally:
            if not self.session:
                db.close()