from controllers.base_controller import BaseController
from models.areas import Area
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AreasController(BaseController):
    def __init__(self, session=None):
        super().__init__(None, Area, session)
        self.session = session
        logger.info("Inicializando AreasController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("AreasController inicializado con éxito.")

    def crear_area(self, nombre):
        if not nombre:
            return False, "El nombre del área es obligatorio."

        db = self.get_db_session()  # Usar el método de la clase madre
        try:
            with db.begin():
                area = Area(area=nombre)
                db.add(area)
                logger.info(f"Área creada: {nombre}")
                return True, "Área creada exitosamente."
        except SQLAlchemyError as e:
            logger.error(f"Error al crear área: {e}")
            return False, f"Error al crear área: {e}. Inténtalo de nuevo."
        finally:
            db.close()

    def actualizar_area(self, id, nombre):
        #Validar los datos
        if not id:
            return False, "El id del área es obligatorio."
        if not nombre:
            return False, "El nombre del área es obligatorio."

        db = self.get_db_session()  # Usar el método de la clase madre
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    area.area = nombre  
                    logger.info(f"Área actualizada: {nombre}")
                    return True, "Área actualizada exitosamente."
                else:
                    return False, "Área no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar área: {e}")
            return False, f"Error al actualizar área: {e}. Inténtalo de nuevo."
        finally:
            db.close()
                
    def eliminar_area(self, id):
        db = self.get_db_session()  # Usar el método de la clase madre
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    db.delete(area)
                    logger.info(f"Área eliminada: {area.area}")
                    return True, "Área eliminada exitosamente."
                else:
                    return False, "Área no encontrada."
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar área: {e}")
            return False, f"Error al eliminar área: {e}. Inténtalo de nuevo."
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def listar_areas(self):
        """Método para listar las áreas y manejar errores."""
        db = self.get_db_session()  # Usar el método de la clase madre
        try:
            areas = db.query(Area).all()
            logger.info(f"{len(areas)} áreas obtenidas de la base de datos.")
            return areas
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener áreas: {e}")
            return []
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def buscar_area(self, id=None, nombre=None):
        """
        Busca un área por ID o nombre.
        Devuelve una tupla (exito, area, mensaje).
        """
        # Validar que al menos uno de los campos esté lleno
        if not id and not nombre:
            return False, None, "Debe proporcionar un ID o un nombre para buscar el área."
        if id and not isinstance(id, int):
            return False, None, "El ID debe ser un número entero."
        if nombre and not isinstance(nombre, str):
            return False, None, "El nombre debe ser una cadena de texto."
            
        #Buscar Área
        area = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="area")
        if area:
            return True, area, "Área encontrada exitosamente."
        else:
            if id:
                return False, None, f"No existe un área con ID {id}."
            elif nombre:
                return False, None, f"No existe un área con nombre '{nombre}'."