import logging
from models.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from components.styled_popup import StyledPopup

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseController:
    def __init__(self, vista=None, model=None, session=None):
        """
        Clase base para controladores.
        :param vista: Vista asociada al controlador.
        :param model: Modelo SQLAlchemy asociado al controlador.
        :param session: Sesión de base de datos opcional.
        """
        self.vista = vista
        self.model = model
        self.session = session or SessionLocal()  # Usar la sesión proporcionada o crear una nueva

    def get_db_session(self):
        """Obtiene una nueva sesión de base de datos."""
        return SessionLocal()

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """
        Muestra un mensaje en un popup.
        :param titulo: Título del popup.
        :param mensaje: Mensaje a mostrar.
        :param tipo: Tipo de mensaje ('info', 'error', 'success').
        """
        StyledPopup.mostrar_popup(titulo, mensaje, tipo)

    def manejar_excepcion(self, e, mensaje_error):
        """
        Maneja excepciones de SQLAlchemy y muestra un mensaje de error.
        :param e: Excepción capturada.
        :param mensaje_error: Mensaje de error a mostrar.
        """
        logger.error(f"{mensaje_error}: {e}")
        self.mostrar_mensaje("Error", f"{mensaje_error}: {e}", tipo="error")

    def ejecutar_transaccion(self, operacion, mensaje_exito=None):
        """
        Ejecuta una operación dentro de una transacción de base de datos.
        :param operacion: Función que contiene la lógica de la operación.
        :param mensaje_exito: Mensaje de éxito a mostrar (opcional).
        """
        db = self.get_db_session()
        try:
            with db.begin():
                operacion(db)
            if mensaje_exito:
                self.mostrar_mensaje("Éxito", mensaje_exito, tipo="success")
        except SQLAlchemyError as e:
            self.manejar_excepcion(e, "Error al ejecutar la operación")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
    
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
            query = db.query(self.model)
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