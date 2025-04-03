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
        area_creada = False
        try:
            with db.begin():
                area = Area(area=nombre)
                db.add(area)
                logger.info(f"Área creada: {nombre}")
                area_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear área: {e}")
            self.vista.mostrar_error("Error al crear área. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_creada:
                self.vista.mostrar_exito("Área creada exitosamente.")
            else:
                self.vista.manager.current = 'lista_areas'

    def actualizar_area(self, id, nombre):
        if not nombre:
            self.vista.mostrar_error("El nombre del área es obligatorio.")
            return

        db = SessionLocal()
        area_actualizada = False
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    area.area = nombre  
                    logger.info(f"Área actualizada: {nombre}")
                    area_actualizada = True
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar área: {e}")
            self.vista.mostrar_error("Error al actualizar área. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_actualizada:
                self.vista.mostrar_exito("Área actualizada exitosamente.")
            else:
                self.vista.manager.current = 'lista_areas' 

    def eliminar_area(self, id):
        db = SessionLocal()
        area_eliminada = False
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    db.delete(area)
                    logger.info(f"Área eliminada: {area.area}")
                    area_eliminada = True
                else:
                    self.vista.mostrar_error("Área no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar área: {e}")
            self.vista.mostrar_error("Error al eliminar área. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_eliminada:
                self.vista.mostrar_exito("Área eliminada exitosamente.")
            else:
                self.vista.manager.current = 'lista_areas'  

    def listar_areas(self, vista):
        """Fetches areas from the database and updates the view."""
        db = SessionLocal()
        try:
            areas = db.query(Area).all()
            logger.info(f"{len(areas)} áreas obtenidas de la base de datos.")
            if hasattr(vista, 'actualizar_lista_areas'):
                vista.actualizar_lista_areas(areas)
            else:
                raise AttributeError("The provided view does not have 'actualizar_lista_areas' method.")
            return areas
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener áreas: {e}")
            self.vista.mostrar_error("Error al obtener áreas. Inténtalo de nuevo.")
            return []
        finally:
            db.close()

    def listar_areas_button_handler(self):
        """Handler for the 'List' button in the areas view."""
        self.listar_areas(self.vista)

    def obtener_area(self, id):
        """Retrieve a single area by its ID."""
        db = SessionLocal()
        try:
            area = db.query(Area).filter(Area.id == id).first()
            if area:
                logger.info(f"Área encontrada: {area.area}")
                return area
            else:
                logger.warning(f"Área con ID {id} no encontrada.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener el área con ID {id}: {e}")
            return None
        finally:
            db.close()
            self.listar_areas()

