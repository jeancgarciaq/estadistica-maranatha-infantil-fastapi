import logging
from models.areas import Area
from models.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AreasController:
    def __init__(self, vista):
        self.vista = vista

    def crear_area(self, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre del área es obligatorio.")
            return

        db = SessionLocal()
        try:
            with db.begin():
                area = Area(area=nombre)  # Corregido: antes usaba "nombre=nombre"
                db.add(area)
                logger.info(f"Área creada: {nombre}")
        except SQLAlchemyError as e:
            logger.error(f"Error al crear área: {e}")
            self.vista.mostrar_error("Error al crear área. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_areas()

    def actualizar_area(self, id, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre del área es obligatorio.")
            return

        db = SessionLocal()
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    area.area = nombre  # Corregido: antes usaba "nombre"
                    logger.info(f"Área actualizada: {nombre}")
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar área: {e}")
            self.vista.mostrar_error("Error al actualizar área. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_areas()

    def eliminar_area(self, id):
        db = SessionLocal()
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    db.delete(area)
                    logger.info(f"Área eliminada: {area.area}")
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar área: {e}")
            self.vista.mostrar_error("Error al eliminar área. Inténtalo de nuevo.")
        finally:
            db.close()
            self.listar_areas()

    def listar_areas_button_handler(self):
        """Handler for the 'List' button in the areas view."""
        self.listar_areas()

    def listar_areas(self, vista):
        """Actualizar el GridLayout de la vista actual con la lista de áreas."""
        db = SessionLocal()
        try:
            areas = db.query(Area).all()
            vista.actualizar_lista_areas(areas)  # Llamar al método de la vista para actualizar la lista
        except SQLAlchemyError as e:
            logger.error(f"Error al listar áreas: {e}")
            vista.mostrar_error("Error al listar áreas. Inténtalo de nuevo.")
        finally:
            db.close()

    def obtener_area(self, id):
        db = SessionLocal()
        try:
            area = db.query(Area).filter(Area.id == id).first()
            return area
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener área: {e}")
            self.vista.mostrar_error("Error al obtener área. Inténtalo de nuevo.")
            return None
        finally:
            db.close()

    def mostrar_mensaje(self, mensaje):
        popup = Popup(title='Información', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
