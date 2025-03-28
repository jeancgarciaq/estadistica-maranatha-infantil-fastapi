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

class ListAreasScreen(Screen):
    def __init__(self, areas, **kwargs):
        super().__init__(**kwargs)
        self.name = 'lista_areas'
        self.areas = areas
        self.ids = {'lista_areas': GridLayout(cols=2, size_hint_y=None)}

    def on_pre_enter(self):
        self.ids['lista_areas'].clear_widgets()
        for area in self.areas:
            self.ids['lista_areas'].add_widget(Label(text=str(area.id)))
            self.ids['lista_areas'].add_widget(Label(text=area.area))

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

    def listar_areas(self):
        print("🟢 Se ejecutó listar_areas()")
        db = SessionLocal()
        try:
            areas = db.query(Area).all()
            self.vista.manager.get_screen('areas_list').actualizar_lista_areas(areas)
            self.vista.manager.current = 'areas_list'
        except SQLAlchemyError as e:
            logger.error(f"Error al listar áreas: {e}")
            self.vista.mostrar_error("Error al listar áreas. Inténtalo de nuevo.")
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

    def mostrar_popup_lista(self):
        areas = self.listar_areas()  # Obtener las áreas

        if not areas:  # Si la lista está vacía, no se muestra el popup
            return  # O puedes mostrar el mensaje aquí si prefieres que sea una sola línea de código

        # Crear el GridLayout y añadir las áreas
        lista_areas_popup = GridLayout(cols=2, size_hint_y=None)
        lista_areas_popup.bind(minimum_height=lista_areas_popup.setter('height'))

        for area in areas:
            lista_areas_popup.add_widget(Label(text=str(area.id)))
            lista_areas_popup.add_widget(Label(text=area.area))

        # Crear el ScrollView para mostrar la lista
        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(lista_areas_popup)

        # Botón para cerrar el popup
        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        # Crear el Popup
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(scrollview)
        popup_content.add_widget(close_button)

        popup = Popup(title='Lista de Áreas', content=popup_content, size_hint=(None, None), size=(400, 400))

        # Cerrar el popup al presionar el botón
        close_button.bind(on_press=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def mostrar_mensaje(self, mensaje):
        popup = Popup(title='Información', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
