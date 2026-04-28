import logging
from models.recepcion import Recepcion
from controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecepcionController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Recepcion, session=session)
        logger.info("RecepcionController inicializado.")

    def crear_recepcion(self, nombre, fecha=None):
        """
        Crea un registro de recepción.
        :return: (Exito, Mensaje)
        """
        if not nombre:
            return False, "El nombre es obligatorio."

        db = self.get_db_session()
        try:
            with db.begin():
                kwargs = {"nombre": nombre}
                if fecha:
                    try:
                        kwargs["fecha"] = datetime.strptime(fecha, '%Y-%m-%d').date()
                    except ValueError:
                        return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
                recepcion = Recepcion(**kwargs)
                db.add(recepcion)
                logger.info(f"Recepción creada.")
            return True, "Recepción creada exitosamente."
        except SQLAlchemyError as e:
            logger.error(f"Error al crear recepción: {e}")
            return False, f"Error al crear recepción: {e}"
        finally:
            db.close()

    def actualizar_recepcion(self, id, nombre, fecha=None):
        """
        Actualiza un registro de recepción.
        :return: (Exito, Mensaje)
        """
        if not nombre:
            return False, "El nombre es obligatorio."

        db = self.get_db_session()
        try:
            with db.begin():
                recepcion = db.query(Recepcion).filter(Recepcion.id == id, Recepcion.is_deleted.is_(False)).first()
                if recepcion:
                    recepcion.nombre = nombre
                    if fecha:
                        try:
                            setattr(recepcion, "fecha", datetime.strptime(fecha, '%Y-%m-%d').date())
                        except ValueError:
                            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
                    logger.info(f"Recepción actualizada: ID {id}")
                    return True, "Recepción actualizada exitosamente."
                else:
                    return False, "Recepción no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar recepción: {e}")
            return False, f"Error al actualizar recepción: {e}"
        finally:
            db.close()

    def eliminar_recepcion(self, id):
        """
        Elimina un registro de recepción.
        :return: (Exito, Mensaje)
        """
        db = self.get_db_session()
        try:
            with db.begin():
                recepcion = db.query(Recepcion).filter(Recepcion.id == id, Recepcion.is_deleted.is_(False)).first()
                if recepcion:
                    self.marcar_eliminado(recepcion, db)
                    logger.info(f"Recepción eliminada: ID {id}")
                    return True, "Recepción eliminada exitosamente."
                else:
                    return False, "Recepción no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar recepción: {e}")
            return False, f"Error al eliminar recepción: {e}"
        finally:
            db.close()

    def listar_recepciones(self):
        """
        Lista todos los registros de recepción.
        :return: Lista de objetos Recepcion.
        """
        db = self.get_db_session()
        try:
            recepciones = db.query(Recepcion).filter(Recepcion.is_deleted.is_(False)).all()
            logger.info("Recepciones listadas.")
            return recepciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar recepciones: {e}")
            return []
        finally:
            db.close()

    def obtener_recepcion(self, id):
        """
        Obtiene un registro de recepción por ID.
        :return: Objeto Recepcion o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Recepcion).filter(Recepcion.id == id, Recepcion.is_deleted.is_(False)).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener recepción: {e}")
            return None
        finally:
            db.close()