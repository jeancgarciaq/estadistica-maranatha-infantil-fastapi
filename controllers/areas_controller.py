from controllers.base_controller import BaseController
from models.areas import Area
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AreasController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Area, session=session)
        logger.info("Inicializando AreasController")

    def _get_db(self, db):
        """Helper para usar la sesión proporcionada o la interna."""
        return db if db else self.session

    def crear_area(self, nombre, user_context=None):
        if not nombre:
            return False, "El nombre del área es obligatorio."

        def operacion(db):
            area = Area(area=nombre)
            db.add(area)
            logger.info(f"Área creada: {nombre}")

        return self.ejecutar_transaccion(operacion, "Área creada exitosamente.", user_context=user_context)

    def actualizar_area(self, id, nombre, user_context=None):
        if not id:
            return False, "El id del área es obligatorio."
        if not nombre:
            return False, "El nombre del área es obligatorio."

        def operacion(db):
            area = self.query_activa(db).filter(Area.id == id).first()
            if not area:
                raise ValueError("Área no encontrada.")
            
            area.area = nombre
            logger.info(f"Área actualizada: {nombre}")

        return self.ejecutar_transaccion(operacion, "Área actualizada exitosamente.", user_context=user_context)
                
    def eliminar_area(self, id, user_context=None):
        if not id:
            return False, "El ID del área es obligatorio."

        def operacion(db):
            area = self.query_activa(db).filter(Area.id == id).first()
            if not area:
                raise ValueError("Área no encontrada.")
            
            self.marcar_eliminado(area, db)
            logger.info(f"Área eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Área eliminada exitosamente.", user_context=user_context)

    def listar_areas(self):
        """Método para listar las áreas y manejar errores."""
        db = self.get_db_session()
        try:
            areas = self.query_activa(db).all()
            logger.info(f"{len(areas)} áreas obtenidas de la base de datos.")
            return areas
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener áreas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def buscar_area(self, id=None, nombre=None):
        """
        Busca un área por ID o nombre.
        Devuelve una tupla (exito, area, mensaje).
        """
        # Validar que al menos uno de los campos esté lleno
        if not id and not nombre:
            return False, None, "Debe proporcionar un ID o un nombre para buscar el área."

        # Intentar convertir ID a int si viene como string
        if id:
            try:
                id = int(id)
            except (ValueError, TypeError):
                return False, None, "El ID proporcionado no es un número válido."

        try:
            area = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="area")
            if area:
                return True, area, "Área encontrada exitosamente."
            return False, None, "No se encontró el área solicitada."
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return False, None, str(e)