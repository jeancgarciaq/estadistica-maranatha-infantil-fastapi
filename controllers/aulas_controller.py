import logging
from models.aulas import Aula
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulasController:
    def __init__(self, vista):
        self.vista = vista

    def crear_aula(self, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, fecha, id_salon):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Creación de aula)
                logger.info(f"Aula creada: {aula.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear aula: {e}")
            self.vista.mostrar_error("Error al crear aula. Inténtalo de nuevo.")
        finally:
            self.listar_aulas()

    def actualizar_aula(self, id, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, fecha, id_salon):
        # ... (Validación de datos)
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Actualización de aula)
                logger.info(f"Aula actualizada: {aula.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar aula: {e}")
            self.vista.mostrar_error("Error al actualizar aula. Inténtalo de nuevo.")
        finally:
            self.listar_aulas()

    def eliminar_aula(self, id):
        db: Session = next(get_db())
        try:
            with db.begin():
                # ... (Eliminación de aula)
                logger.info(f"Aula eliminada: {aula.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar aula: {e}")
            self.vista.mostrar_error("Error al eliminar aula. Inténtalo de nuevo.")
        finally:
            self.listar_aulas()

    def listar_aulas(self):
        db: Session = next(get_db())
        try:
            aulas = db.query(Aula).all()
            self.vista.actualizar_lista_aulas(aulas)
            logger.info("Aulas listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar aulas: {e}")
            self.vista.mostrar_error("Error al listar aulas. Inténtalo de nuevo.")

    def obtener_aula(self, id):
        db: Session = next(get_db())
        try:
            return db.query(Aula).filter(Aula.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener aula: {e}")
            self.vista.mostrar_error("Error al obtener aula. Inténtalo de nuevo.")
            return None