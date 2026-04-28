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
        logger.info("Inicializando LogisticaController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("LogisticaController inicializado con éxito.")

    def crear_logistica(self, datos):
        """
        Crea un nuevo registro de logística en la base de datos.
        :param datos: Diccionario con los datos de la logística.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        db = self.get_db_session()
        try:
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                logistica = Logistica(**datos)
                db.add(logistica)
                logger.info(f"Logística creada.")
            return True, "Logística creada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear logística")
        finally:
            db.close()

    def actualizar_logistica(self, id, datos):
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

        db = self.get_db_session()
        try:
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
                if logistica:
                    for key, value in datos.items():
                        setattr(logistica, key, value)
                    logger.info(f"Logística actualizada: ID {id}")
                    return True, "Logística actualizada exitosamente."
                else:
                    return False, "Logística no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar logística")
        finally:
            db.close()

    def eliminar_logistica(self, id):
        """
        Elimina un registro de logística por su ID.
        :param id: ID de la logística a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la logística es obligatorio y debe ser un número entero."

        db = self.get_db_session()
        try:
            with db.begin():
                logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
                if not logistica:
                    return False, "Logística no encontrada."
                self.marcar_eliminado(logistica, db)
                logger.info(f"Logística eliminada: ID {id}")
            return True, "Logística eliminada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar logística")
        finally:
            db.close()

    def listar_logisticas(self, fecha=None):
        """
        Lista los registros de logística, opcionalmente filtrados por fecha.
        """
        db = self.get_db_session()
        try:
            query = db.query(Logistica).filter(Logistica.is_deleted.is_(False))

            if fecha:
                if isinstance(fecha, str):
                    try:
                        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                    except ValueError:
                        logger.warning(f"Fecha de filtro inválida recibida: {fecha}")
                        return []
                query = query.filter(Logistica.fecha == fecha)

            logisticas = query.order_by(Logistica.fecha.desc(), Logistica.id.desc()).all()
            logger.info(f"{len(logisticas)} registros de logística obtenidos.")
            return logisticas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar logísticas: {e}")
            return []
        finally:
            db.close()

    def obtener_logistica(self, id):
        """
        Obtiene un registro de logística por su ID.
        :param id: ID de la logística.
        :return: Objeto Logistica o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener logística: {e}")
            return None
        finally:
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