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
        logger.info("SalonesController inicializado.")

    def crear_salon(self, nombre, edad, user_context=None):
        if not nombre:
            return False, "El nombre del salón es obligatorio."
        if not edad:
            return False, "La edad del salón es obligatoria."

        def operacion(db):
            salon = Salon(salon=nombre, edad=edad)
            db.add(salon)
            db.flush()
            self.registrar_evento_sync(db, 'salones', salon, 'upsert')
            logger.info(f"Salón creado: {nombre}")

        return self.ejecutar_transaccion(operacion, "Salón creado exitosamente.", user_context=user_context)

    def actualizar_salon(self, id, nombre, edad, user_context=None):
        if not id:
            return False, "El ID del salón es obligatorio."
        if not nombre:
            return False, "El nombre del salón es obligatorio."
        if not edad:
            return False, "La edad del salón es obligatoria."

        def operacion(db):
            salon = self.query_activa(db).filter(Salon.id == id).first()
            if not salon:
                raise ValueError("Salón no encontrado.")
            
            salon.salon = nombre
            salon.edad = edad
            self.registrar_evento_sync(db, 'salones', salon, 'upsert')
            logger.info(f"Salón actualizado: {nombre}")

        return self.ejecutar_transaccion(operacion, "Salón actualizado exitosamente.", user_context=user_context)

    def eliminar_salon(self, id, user_context=None):
        if not id:
            return False, "El ID del salón es obligatorio."

        def operacion(db):
            salon = self.query_activa(db).filter(Salon.id == id).first()
            if not salon:
                raise ValueError("Salón no encontrado.")
            
            self.marcar_eliminado(salon, db)
            self.registrar_evento_sync(db, 'salones', salon, 'delete')
            logger.info(f"Salón eliminado: ID {id}")

        return self.ejecutar_transaccion(operacion, "Salón eliminado exitosamente.", user_context=user_context)

    def listar_salones(self):
        """Método para listar los salones y manejar errores."""
        db = self.get_db_session()
        try:
            salones = self.query_activa(db).all()
            logger.info(f"{len(salones)} salones obtenidos de la base de datos.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_salon(self, id):
        """Obtiene un salón por su ID."""
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Salon.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salón: {e}")
            return None
        finally:
            if not self.session:
                db.close()

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