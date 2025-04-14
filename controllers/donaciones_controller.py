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

    def crear_donacion(self, cantidad, descripcion, unidad, equipo, fecha):
        #Validacion de datos sencilla
        if not cantidad or not descripcion or not unidad or not equipo or not fecha:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return
        db: SessionLocal()
        donacion_creada = False
        try:
            with db.begin():
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                donacion = Donacion(
                    cantidad=float(cantidad),
                    descripcion=descripcion,
                    unidad=unidad,
                    equipo=equipo,
                    fecha=fecha_obj,
                )
                db.add(donacion)
                logger.info(f"Donación creada: {donacion.id}")
                donacion_creada = True
        except ValueError:
            self.vista.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear donación: {e}")
            self.vista.mostrar_error("Error al crear donación. Inténtalo de nuevo.")
        finally:
            db.close()
            if donacion_creada:
                self.vista.mostrar_exito("Donación creada exitosamente.")

    def actualizar_donacion(self, donacion_id, cantidad, descripcion, unidad, equipo, fecha):
        # Validación de datos
        if not donacion_id or not cantidad or not descripcion or not unidad or not equipo or not fecha:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return
            
        db: SessionLocal()
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