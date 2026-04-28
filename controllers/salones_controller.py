import logging
from controllers.base_controller import BaseController
from models.salones import Salon
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Salon, session=session)
        logger.info("Inicializando SalonesController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("SalonesController inicializado con éxito.")

    def crear_salon(self, nombre, edad):
        if not nombre:
            return False, "El nombre del salón es obligatorio."
        if not edad:
            return False, "La edad del salón es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                salon = Salon(salon=nombre, edad=edad)
                db.add(salon)
                logger.info(f"Salón creado: {nombre}")
            return True, "Salón creado exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear salón")
        finally:
            db.close()

    def actualizar_salon(self, id, nombre, edad):
        if not id:
            return False, "El ID del salón es obligatorio."
        if not nombre:
            return False, "El nombre del salón es obligatorio."
        if not edad:
            return False, "La edad del salón es obligatoria."

        db = self.get_db_session()
        try:
            with db.begin():
                salon = db.query(Salon).filter(Salon.id == id).first()
                if salon:
                    salon.salon = nombre  
                    salon.edad = edad
                    logger.info(f"Salón actualizado: {nombre}")
                    return True, "Salón actualizado exitosamente."
                else:
                    return False, "Salón no encontrado."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar salón")
        finally:
            db.close()
                
    def eliminar_salon(self, id):
        if not id:
            return False, "El ID del salón es obligatorio."

        db = self.get_db_session()
        try:
            with db.begin():
                salon = db.query(Salon).filter(Salon.id == id).first()
                if salon:
                    db.delete(salon)
                    logger.info(f"Salón eliminado: ID {id}")
                    return True, "Salón eliminado exitosamente."
                else:
                    return False, "Salón no encontrado."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar salón")
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def listar_salones(self):
        """Método para listar los salones y manejar errores."""
        db = self.get_db_session()
        try:
            salones = db.query(Salon).all()
            logger.info(f"{len(salones)} salones obtenidos de la base de datos.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salones: {e}")
            return []
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def obtener_salon(self, id):
        """Obtiene un salón por su ID."""
        db = self.get_db_session()
        try:
            return db.query(Salon).filter(Salon.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salón: {e}")
            return None
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def buscar_salon(self, id=None, nombre=None):
        """
        Busca un salón por ID o nombre.
        :param id: ID del salón a buscar.
        :param nombre: Nombre del salón a buscar.
        :return: (Exito, Objeto, Mensaje)
        """
        # Validar datos
        if not id and not nombre:
            return False, None, "Debe proporcionar un ID o un nombre para buscar el salón."
        if id and not isinstance(id, int):
            return False, None, "El ID debe ser un número entero."
        if nombre and not isinstance(nombre, str):
            return False, None, "El nombre debe ser una cadena de texto."
            
        salon = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="salon")
        if salon:
            return True, salon, "Salón encontrado exitosamente."
        else:
            if id:
                return False, None, f"No existe un salón con ID {id}."
            elif nombre:
                return False, None, f"No existe un salón con nombre '{nombre}'."
            return False, None, "Salón no encontrado."