import logging
from models.donaciones import Donacion
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonacionesController:
    def __init__(self, vista):
        self.vista = vista

    def crear_donacion(self, cantidad, descripcion, unidad, fecha, equipo, salones_ids):
        db: Session = next(get_db())
        try:
            with db.begin():
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                nueva_donacion = Donacion(
                    cantidad=float(cantidad),
                    descripcion=descripcion,
                    unidad=unidad,
                    fecha=fecha_obj,
                    equipo=equipo
                )
                for salon_id in salones_ids:
                    salon = db.query(Salon).filter(Salon.id == salon_id).first()
                    if salon:
                        nueva_donacion.salones.append(salon)
                db.add(nueva_donacion)
                logger.info(f"Donación creada: {nueva_donacion.id}")
        except ValueError:
            self.vista.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear donación: {e}")
            self.vista.mostrar_error("Error al crear donación. Inténtalo de nuevo.")
        finally:
            self.vista.listar_donaciones()

    def actualizar_donacion(self, donacion_id, cantidad, descripcion, unidad, fecha, equipo, salones_ids):
        db: Session = next(get_db())
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
                if donacion:
                    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                    donacion.cantidad = float(cantidad)
                    donacion.descripcion = descripcion
                    donacion.unidad = unidad
                    donacion.fecha = fecha_obj
                    donacion.equipo = equipo
                    donacion.salones.clear()
                    for salon_id in salones_ids:
                        salon = db.query(Salon).filter(Salon.id == salon_id).first()
                        if salon:
                            donacion.salones.append(salon)
                    logger.info(f"Donación actualizada: {donacion.id}")
                else:
                    self.vista.mostrar_error("Donación no encontrada.")
        except ValueError:
            self.vista.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar donación: {e}")
            self.vista.mostrar_error("Error al actualizar donación. Inténtalo de nuevo.")
        finally:
            self.vista.listar_donaciones()

    def eliminar_donacion(self, donacion_id):
        db: Session = next(get_db())
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
                if donacion:
                    db.delete(donacion)
                    logger.info(f"Donación eliminada: {donacion_id}")
                else:
                    self.vista.mostrar_error("Donación no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar donación: {e}")
            self.vista.mostrar_error("Error al eliminar donación. Inténtalo de nuevo.")
        finally:
            self.vista.listar_donaciones()

    def listar_donaciones(self):
        db: Session = next(get_db())
        try:
            donaciones = db.query(Donacion).all()
            self.vista.actualizar_lista_donaciones(donaciones)
            logger.info("Donaciones listadas.")
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            self.vista.mostrar_error("Error al listar donaciones. Inténtalo de nuevo.")