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
from kivy.uix.widget import Widget

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
            self.vista.mostrar_error(f"Error al crear área: {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_creada:
                self.vista.mostrar_exito("Área creada exitosamente.")

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
            self.vista.mostrar_error(f"Error al actualizar área: {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_actualizada:
                self.vista.mostrar_exito("Área actualizada exitosamente.")

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
            self.vista.mostrar_error(f"Error al eliminar área: {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if area_eliminada:
                self.vista.mostrar_exito("Área eliminada exitosamente.")

    def listar_areas(self, vista):
        """Método para listar las áreas y manejar errores.."""
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
            self.vista.mostrar_error(f"Error al obtener áreas: {e}. Inténtalo de nuevo.")
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
                self.mostrar_area(f"Área encontrada: {area.area}")
                return area
            else:
                logger.warning(f"Área con ID {id} no encontrada.")
                self.vista.mostrar_ernor(f"Error al encontrar área: {id}, no existe.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener el área con ID {id}: {e}")
            self.vista.mostrar_ernor(f"Error al obtener el área con ID {id}: {e}.")
            return None
        finally:
            db.close()

    def mostrar_area(self, mensaje):
        """Display a popup with the area message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)  # Updated background color
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)  # Updated text color to white
        )
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0, 119/255, 194/255, 1),
            size_hint_y=None,
            height=50
        )
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Información del Área",
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),  # Updated title text color to white
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def mostrar_ernor(self, mensaje):
        """Display a popup with the error message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)  # Updated background color
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)  # Updated text color to white
        )
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0, 119/255, 194/255, 1),
            size_hint_y=None,
            height=50
        )
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Error",  
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),  # Updated title text color to white
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()


