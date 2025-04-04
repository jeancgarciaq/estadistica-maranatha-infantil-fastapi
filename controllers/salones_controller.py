import logging
from models.salones import Salon
from models.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonesController:
    def __init__(self, vista=None):
        self.vista = vista 

    def crear_salon(self, salon, edad):

        # Validación de datos
        if not salon:
            self.vista.mostrar_error("El nombre del salón es obligatorio.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del salón es obligatoria.")
            return
        db = SessionLocal()
        try:
            with db.begin():
                nuevo_salon = Salon(nombre=salon, edad=edad)  # Crear instancia de Salon
                db.add(nuevo_salon)  # Agregar a la base de datos
                logger.info(f"Salón creado: {nuevo_salon.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear salón: {e}")
            self.vista.mostrar_error("Error al crear salón. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_salones()

    def actualizar_salon(self, id, salon, edad):
        # Validación de datos
        if not id:
            self.vista.mostrar_error("El ID del salón es obligatorio.")
            return
        if not salon:
            self.vista.mostrar_error("El nombre del salón es obligatorio.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del salón es obligatoria.")
            return

        db = SessionLocal()
        try:
            with db.begin():
                salon_existente = db.query(Salon).filter(Salon.id == id).first()
                if not salon_existente:
                    self.vista.mostrar_error("El salón no existe.")
                    return
                salon_existente.nombre = salon
                salon_existente.edad = edad
                logger.info(f"Salón actualizado: {salon_existente.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar salón: {e}")
            self.vista.mostrar_error("Error al actualizar salón. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_salones()

    def eliminar_salon(self, id):
        # Validación de datos
        if not id:
            self.vista.mostrar_error("El ID del salón es obligatorio.")
            return

        db = SessionLocal()
        try:
            with db.begin():
                salon_existente = db.query(Salon).filter(Salon.id == id).first()
                if not salon_existente:
                    self.vista.mostrar_error("El salón no existe.")
                    return
                db.delete(salon_existente)  # Eliminar el salón de la base de datos
                logger.info(f"Salón eliminado: {salon_existente.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar salón: {e}")
            self.vista.mostrar_error("Error al eliminar salón. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_salones()

    def listar_salones(self, from_button=False):
        """
        Método para listar los salones y manejar errores.
        """
        db = SessionLocal()
        try:
            with db.begin():
                salones = db.query(Salon).all()  
                if self.vista:
                    self.vista.actualizar_lista_salones(salones) 
                logger.info("Salones listados correctamente.")
                if from_button:
                    logger.info("Botón 'Listar' presionado y salones listados correctamente.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones: {e}")
            self.vista.mostrar_error("Error al listar salones. Inténtalo de nuevo.")
        finally:
            db.close()

    def obtener_salon(self, id):
        """Retrieve a single salon by its ID."""
        db = SessionLocal()
        try:
            salon = db.query(Salon).filter(Salon.id == id).first()
            if salon:
                logger.info(f"Salon encontrado: {salon.salon}")
                return salon
            else:
                logger.warning(f"Salon con ID {id} no encontrado.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener el salón con ID {id}: {e}")
            return None
        finally:
            db.close()