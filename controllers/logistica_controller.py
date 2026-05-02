import logging
from models.logistica import Logistica # Assuming this model exists
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from controllers.base_controller import BaseController # Assuming BaseController exists

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogisticaController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Logistica, session=session)
        logger.info("LogisticaController inicializado.")

    def crear_logistica(self, datos, user_context=None):
        """
        Crea un nuevo registro de logística en la base de datos.
        :param datos: Diccionario con los datos de la logística.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        fecha_dt = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha_dt

        def operacion(db):
            logistica = Logistica(**datos)
            db.add(logistica)
            db.flush()
            self.registrar_evento_sync(db, 'logistica', logistica, 'upsert')
            logger.info("Logística creada.")

        return self.ejecutar_transaccion(operacion, "Logística creada exitosamente.", user_context=user_context)

    def actualizar_logistica(self, id, datos, user_context=None):
        """
        Actualiza un registro de logística existente.
        :param id: ID de la logística a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la logística es obligatorio y debe ser un número entero."

        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        fecha_dt = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha_dt

        def operacion(db):
            logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
            if not logistica:
                raise ValueError("Logística no encontrada.")
            
            for key, value in datos.items():
                setattr(logistica, key, value)
            
            self.registrar_evento_sync(db, 'logistica', logistica, 'upsert')
            logger.info(f"Logística actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Logística actualizada exitosamente.", user_context=user_context)

    def eliminar_logistica(self, id, user_context=None):
        """
        Elimina un registro de logística por su ID.
        :param id: ID de la logística a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la logística es obligatorio y debe ser un número entero."

        def operacion(db):
            logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
            if not logistica:
                raise ValueError("Logística no encontrada.")
            
            self.marcar_eliminado(logistica, db)
            self.registrar_evento_sync(db, 'logistica', logistica, 'delete')
            logger.info(f"Logística eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Logística eliminada exitosamente.", user_context=user_context)

    def listar_logisticas(self, fecha=None):
        """
        Lista los registros de logística, opcionalmente filtrados por fecha.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db)

            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(Logistica.fecha == fecha_dt)

            logisticas = query.order_by(Logistica.fecha.desc(), Logistica.id.desc()).all()
            logger.info(f"{len(logisticas)} registros de logística obtenidos.")
            return logisticas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar logísticas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_logistica(self, id):
        """
        Obtiene un registro de logística por su ID.
        :param id: ID de la logística.
        :return: Objeto Logistica o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Logistica.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener logística: {e}")
            return None
        finally:
            if not self.session:
                db.close()

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar una logística.
        :param datos: Diccionario con los datos de la logística.
        :return: Lista de errores encontrados.
        """
        errores = []
        if not isinstance(datos.get("almacen"), str) or not datos.get("almacen").strip():
            errores.append("El campo 'almacen' es obligatorio.")
        if not isinstance(datos.get("capitan"), str) or not datos.get("capitan").strip():
            errores.append("El campo 'capitan' es obligatorio.")
        if not isinstance(datos.get("fecha"), str):
            errores.append("El campo 'fecha' debe ser una cadena de texto con formato 'YYYY-MM-DD'.")
        else:
            try:
                datetime.strptime(datos["fecha"], '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")
        return errores