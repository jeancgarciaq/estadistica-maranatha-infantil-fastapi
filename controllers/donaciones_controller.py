import logging
from models.donaciones import Donacion
from models.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from components.styled_popup import StyledPopup

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonacionesController:
    def __init__(self, vista):
        self.vista = vista

    def crear_donacion(self, cantidad, descripcion, unidad, equipo, fecha):
        """Crea una nueva donación en la base de datos."""
        # Validación de datos
        if not cantidad or not descripcion or not unidad or not equipo or not fecha:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return

        try:
            cantidad = float(cantidad)
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.vista.mostrar_error("Formato de datos incorrecto. Verifique la cantidad y la fecha.")
            return

        db = None
        donacion_creada = False
        try:
            db = SessionLocal()
            with db.begin():
                donacion = Donacion(
                    cantidad=cantidad,
                    descripcion=descripcion,
                    unidad=unidad,
                    equipo=equipo,
                    fecha=fecha,
                )
                db.add(donacion)
                logger.info(f"Donación creada: {donacion.id}")
                donacion_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear donación: {e}")
            self.vista.mostrar_error("Error al crear donación. Inténtalo de nuevo.")
        finally:
            if db:
                db.close()
            if donacion_creada:
                self.vista.mostrar_exito("Donación creada exitosamente.")

    def actualizar_donacion(self, donacion_id, cantidad, descripcion, unidad, equipo, fecha):
        # Validación de datos
        if not donacion_id or not cantidad or not descripcion or not unidad or not equipo or not fecha:
            self.vista.mostrar_error("Todos los campos son obligatorios.")
            return
            
        db = SessionLocal()
        donacion_actualizada = False
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
                if donacion:
                    donacion.cantidad = float(cantidad)
                    donacion.descripcion = descripcion
                    donacion.unidad = unidad
                    donacion.fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                    donacion.equipo = equipo
                    donacion_actualizada = True
                    logger.info(f"Donación actualizada: {donacion.id}")
                else:
                    self.vista.mostrar_error("Donación no encontrada.")
        except ValueError:
            self.vista.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar donación: {e}")
            self.vista.mostrar_error("Error al actualizar donación. Inténtalo de nuevo.")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
            if donacion_actualizada:
                self.vista.mostrar_exito("Donación actualizada exitosamente.")

    def eliminar_donacion(self, donacion_id):
        # Validación de datos
        if not donacion_id:
            self.vista.mostrar_error("ID de donación es obligatorio.")
            return

        db = SessionLocal()
        donacion_eliminada = False
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
                if donacion:
                    db.delete(donacion)
                    donacion_eliminada = True
                    logger.info(f"Donación eliminada: {donacion_id}")
                else:
                    self.vista.mostrar_error("Donación no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar donación: {e}")
            self.vista.mostrar_error("Error al eliminar donación. Inténtalo de nuevo.")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
            if donacion_eliminada:
                self.vista.mostrar_exito("Donación eliminada exitosamente.")

    def listar_donaciones(self):
        """Obtiene la lista de donaciones desde la base de datos."""
        db = None
        try:
            db = SessionLocal()
            donaciones = db.query(Donacion).all()
            logger.info(f"{len(donaciones)} donaciones obtenidas de la base de datos.")
            if hasattr(self.vista, 'actualizar_lista_donaciones'):
                self.vista.actualizar_lista_donaciones(donaciones)
            else:
                raise AttributeError("La vista no tiene el método 'actualizar_lista_donaciones'.")
            return donaciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            if hasattr(self.vista, 'mostrar_error'):
                self.vista.mostrar_error("Error al listar donaciones. Inténtalo de nuevo.")
            return []
        finally:
            if db:
                db.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def listar_donaciones_button_handler(self):
        """Método para manejar el evento de listar donaciones."""
        self.listar_donaciones(self.vista)
    
    def obtener_donacion(self, id=None, fecha=None):
        if not id and not fecha:
            self.vista.mostrar_error("Debes proporcionar un ID o una fecha para obtener la donación.")
            return None
        db = SessionLocal()
        try:
            db.query(Donacion)
            if id:
                donacion = db.query(Donacion).filter(Donacion.id == id).first()
            else:
                donacion = db.query(Donacion).filter(Donacion.fecha == fecha).first()

            if donacion:
                logger.info(f"Donación encontrada: {donacion.id}")
                self.mostrar_popup(f"Donación encontrada: {donacion.id}, {donacion.fecha}")
                return donacion
            else:
                if id:
                    logger.warning(f"Donación con ID {id} no encontrada.")
                    self.vista.mostrar_error("Donación no encontrada.")
                elif fecha:
                    logger.warning(f"Donación con fecha {fecha} no encontrada.")
                    self.vista.mostrar_error("Donación no encontrada.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener donación: {e}")
            self.vista.mostrar_error("Error al obtener donación. Inténtalo de nuevo.")
            return None
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
    
    def mostrar_popup(self, mensaje, titulo="Información"):
        """Muestra un popup con un mensaje."""
        try:
            popup_content = StyledPopup()
            if isinstance(mensaje, dict):
                # Si el mensaje es un diccionario, mostrar pares clave-valor
                popup_content.set_content(mensaje)
            else:
                # Si el mensaje es un texto, mostrarlo directamente
                popup_content.ids.popup_label.text = mensaje

            popup = Popup(
                title=titulo,
                content=popup_content,
                size_hint=(0.8, 0.4),
                title_align="center",
                title_color=(1, 1, 1, 1),  # Título en blanco
            )
            popup_content.ids.close_button.bind(on_release=popup.dismiss)  # Vincular el botón de cerrar
            popup.open()
        except Exception as e:
            logger.error(f"Error al mostrar el popup: {e}")