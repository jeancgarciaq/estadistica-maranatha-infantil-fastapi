import logging
from models.recepcion import Recepcion
from controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecepcionController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Recepcion, session=session)
        logger.info("RecepcionController inicializado.")

    def crear_recepcion(self, nombre, fecha=None, user_context=None):
        """
        Crea un registro de recepción.
        :return: (Exito, Mensaje)
        """
        if not nombre:
            return False, "El nombre es obligatorio."

        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if fecha and not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

        def operacion(db):
            recepcion = Recepcion(nombre=nombre, fecha=fecha_dt)
            db.add(recepcion)
            db.flush()
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'upsert')
            logger.info("Recepción creada.")

        return self.ejecutar_transaccion(operacion, "Recepción creada exitosamente.", user_context=user_context)

    def actualizar_recepcion(self, id, nombre, fecha=None, user_context=None):
        """
        Actualiza un registro de recepción.
        :return: (Exito, Mensaje)
        """
        if not nombre:
            return False, "El nombre es obligatorio."

        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if fecha and not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

        def operacion(db):
            recepcion = self.query_activa(db).filter(Recepcion.id == id).first()
            if not recepcion:
                raise ValueError("Recepción no encontrada.")
            
            recepcion.nombre = nombre
            if fecha_dt:
                recepcion.fecha = fecha_dt
            
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'upsert')
            logger.info(f"Recepción actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Recepción actualizada exitosamente.", user_context=user_context)

    def eliminar_recepcion(self, id, user_context=None):
        """
        Elimina un registro de recepción.
        :return: (Exito, Mensaje)
        """
        def operacion(db):
            recepcion = self.query_activa(db).filter(Recepcion.id == id).first()
            if not recepcion:
                raise ValueError("Recepción no encontrada.")
            
            self.marcar_eliminado(recepcion, db)
            self.registrar_evento_sync(db, 'recepciones', recepcion, 'delete')
            logger.info(f"Recepción eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Recepción eliminada exitosamente.", user_context=user_context)

    def listar_recepciones(self, fecha=None):
        """
        Lista todos los registros de recepción.
        :return: Lista de objetos Recepcion.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(Recepcion.fecha == fecha_dt)
            
            recepciones = query.order_by(Recepcion.id.desc()).all()
            logger.info("Recepciones listadas.")
            return recepciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar recepciones: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_recepcion(self, id):
        """
        Obtiene un registro de recepción por ID.
        :return: Objeto Recepcion o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Recepcion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener recepción: {e}")
            return None
        finally:
            if not self.session:
                db.close()