from controllers.base_controller import BaseController
from models.recepcion import Recepcion
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecepcionController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Recepcion, session=session)
        logger.info("RecepcionController inicializado.")

    def crear_recepcion(self, nombre, fecha, user_context=None):
        if not nombre or not fecha:
            return False, "El nombre y la fecha son obligatorios."

        fecha_obj = self.validar_y_convertir_fecha(fecha)
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            recepcion = Recepcion(nombre=nombre, fecha=fecha_obj)
            db.add(recepcion)
            db.flush()
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'upsert')
            logger.info(f"Recepción creada: {nombre}")

        return self.ejecutar_transaccion(operacion, "Recepción registrada exitosamente.", user_context=user_context)

    def actualizar_recepcion(self, id, nombre, fecha, user_context=None):
        if not id or not nombre or not fecha:
            return False, "Todos los campos son obligatorios para actualizar."

        fecha_obj = self.validar_y_convertir_fecha(fecha)
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            recepcion = self.query_activa(db).filter(Recepcion.id == id).first()
            if not recepcion:
                raise ValueError("Recepción no encontrada.")
            
            recepcion.nombre = nombre
            recepcion.fecha = fecha_obj
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'upsert')
            logger.info(f"Recepción actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Recepción actualizada exitosamente.", user_context=user_context)
                
    def eliminar_recepcion(self, id, user_context=None):
        if not id:
            return False, "El ID de la recepción es obligatorio."

        def operacion(db):
            recepcion = self.query_activa(db).filter(Recepcion.id == id).first()
            if not recepcion:
                raise ValueError("Recepción no encontrada.")
            
            self.marcar_eliminado(recepcion, db)
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'delete')
            logger.info(f"Recepción eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Recepción eliminada exitosamente.", user_context=user_context)

    def listar_recepciones(self):
        """Lista todas las recepciones activas ordenadas por fecha reciente."""
        db = self.get_db_session()
        try:
            recepciones = self.query_activa(db).order_by(Recepcion.fecha.desc(), Recepcion.id.desc()).all()
            logger.info(f"{len(recepciones)} recepciones obtenidas.")
            return recepciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar recepciones: {e}")
            return []
        finally:
            if not self.session:
                db.close()