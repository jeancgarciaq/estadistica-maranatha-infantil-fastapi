import logging
from models.donaciones import Donacion
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistribucionController:
    def __init__(self, vista):
        self.vista = vista

    def obtener_donaciones(self):
        db: Session = next(get_db())
        try:
            donaciones = db.query(Donacion).all()
            return [f"{donacion.id}: {donacion.descripcion}" for donacion in donaciones]
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener donaciones: {e}")
            self.vista.mostrar_error("Error al obtener donaciones. Inténtalo de nuevo.")
            return []

    def obtener_salones(self):
        db: Session = next(get_db())
        try:
            salones = db.query(Salon).all()
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salones: {e}")
            self.vista.mostrar_error("Error al obtener salones. Inténtalo de nuevo.")
            return []

    def registrar_distribucion(self, donacion_id, salones_ids):
        db: Session = next(get_db())
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
                if donacion:
                    donacion.salones.clear()  # Limpia los salones existentes
                    for salon_id in salones_ids:
                        salon = db.query(Salon).filter(Salon.id == salon_id).first()
                        if salon:
                            donacion.salones.append(salon)
                    logger.info(f"Distribución registrada: Donación {donacion_id}, Salones {salones_ids}")
                else:
                    self.vista.mostrar_error("Donación no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al registrar distribución: {e}")
            self.vista.mostrar_error("Error al registrar distribución. Inténtalo de nuevo.")
        finally:
            self.vista.listar_distribuciones() # Actualizar la lista de distribución

    def listar_distribuciones(self):
        db: Session = next(get_db())
        try:
            donaciones = db.query(Donacion).filter(Donacion.salones.any()).all() # Obtener donaciones con salones asignados
            self.vista.actualizar_lista_distribuciones(donaciones)
            logger.info("Distribuciones listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar distribuciones: {e}")
            self.vista.mostrar_error("Error al listar distribuciones. Inténtalo de nuevo.")