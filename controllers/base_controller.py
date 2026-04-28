import logging
from datetime import datetime, date

from models.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from utils.firebase_sync import SyncManager

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseController:
    def __init__(self, vista=None, model=None, session=None):
        """
        Clase base para controladores.
        :param vista: (DEPRECATED) Vista asociada al controlador. Mantenido por compatibilidad temporal.
        :param model: Modelo SQLAlchemy asociado al controlador.
        :param session: Sesión de base de datos opcional.
        """
        self.vista = vista
        self.model = model
        self.session = session or SessionLocal()
        self.sync_manager = SyncManager()

    def get_db_session(self):
        """Obtiene una nueva sesión de base de datos."""
        return SessionLocal()

    def manejar_excepcion(self, e, mensaje_error):
        """
        Maneja excepciones de SQLAlchemy y devuelve un mensaje formateado.
        :param e: Excepción capturada.
        :param mensaje_error: Mensaje base de error.
        :return: (False, Mensaje de error formateado)
        """
        logger.error(f"{mensaje_error}: {e}")
        return False, f"{mensaje_error}: {e}"

    def validar_y_convertir_fecha(self, fecha):
        """Valida y convierte una fecha de string a objeto date."""
        if isinstance(fecha, date):
            return fecha
        if not isinstance(fecha, str):
            return None
        try:
            return datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            logger.error(f"Formato de fecha inválido: {fecha}")
            return None

    def ejecutar_transaccion(self, operacion, mensaje_exito=None):
        """
        Ejecuta una operación dentro de una transacción de base de datos.
        :param operacion: Función que contiene la lógica de la operación.
        :param mensaje_exito: Mensaje de éxito a devolver (opcional).
        :return: Tupla (Booleano Exito, Mensaje)
        """
        db = self.get_db_session()
        try:
            with db.begin():
                operacion(db)
            if mensaje_exito:
                return True, mensaje_exito
            return True, "Operación exitosa"
        except (SQLAlchemyError, ValueError) as e:
            return self.manejar_excepcion(e, "Error en la transacción")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")

    def marcar_eliminado(self, registro, db):
        """Marca un registro como eliminado sin borrarlo físicamente."""
        if registro is None:
            return False

        if hasattr(registro, 'is_deleted'):
            registro.is_deleted = True

        if hasattr(registro, 'updated_at'):
            registro.updated_at = datetime.utcnow()

        db.add(registro)
        return True

    def registrar_evento_sync(self, db, entity_name, registro, operation='upsert'):
        """Encola un cambio local para sincronización con Firebase."""
        return self.sync_manager.enqueue_model(db, entity_name, registro, operation=operation)

    def query_activa(self, db):
        """Devuelve una query filtrada por registros activos cuando el modelo lo soporta."""
        query = db.query(self.model)
        if hasattr(self.model, 'is_deleted'):
            return query.filter(self.model.is_deleted.is_(False))
        return query
    
    def buscar_por_id_o_nombre(self, id=None, nombre=None, nombre_campo="nombre"):
        """
        Busca un registro por ID o nombre.
        :param id: ID del registro a buscar.
        :param nombre: Nombre del registro a buscar.
        :param nombre_campo: Nombre del campo en el modelo para buscar por nombre.
        :return: El registro encontrado o None.
        """
        if not id and not nombre:
            logger.warning("Debe proporcionar un ID o un nombre para buscar.")
            return None

        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if id:
                registro = query.filter(self.model.id == id).first()
            elif nombre:
                registro = query.filter(getattr(self.model, nombre_campo) == nombre).first()

            if registro:
                logger.info(f"Registro encontrado: {registro}")
                return registro
            else:
                logger.warning(f"No se encontró un registro con {'ID ' + str(id) if id else nombre_campo + ' ' + nombre}.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar registro. ID: {id}, Nombre: {nombre}, Error: {e}")
            return None
        finally:
            db.close()
            logger.info("Conexión cerrada.")

    def buscar_por_id_o_fecha(self, id=None, fecha=None, nombre_campo="nombre"):
        """
        Busca un registro por ID o fecha:
        :param id: El ID del registro a buscar
        :param fecha: La fecha del registro a buscar
        :param nombre_campo: Nombre del campo en el modelo para buscar por nombre.
        :return: El registro encontrado o None
        """
        #Validacion sencilla
        if not id and not fecha:
            logger.warning("Debe proporcionar un id o fecha a buscar")
            return None
        
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if id:
                registro = query.filter(self.model.id == id).first()
            elif fecha:
                registro = query.filter(getattr(self.model, nombre_campo) == fecha).first()

            if registro:
                logger.info(f"Registro encontrado: {registro}")
                return registro
            else:
                logger.warning(f"No se encontró un registro con {'ID ' + str(id) if id else nombre_campo + ' ' + str(fecha)}.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar registro. ID: {id}, Fecha: {fecha}, Error: {e}")
            return None
        finally:
            db.close()
            logger.info("Conexión cerrada.")


    