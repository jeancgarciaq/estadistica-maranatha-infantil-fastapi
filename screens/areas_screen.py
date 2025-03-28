import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from controllers import AreasController
import logging


# Configuración de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class AreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        # Cargar el archivo KV dentro del try-except
        try:
            Builder.load_file('views/areas.kv')
        except Exception as e:
            print(f"Error al cargar areas.kv: {e}")
        super().__init__(**kwargs)
        # Crear el controlador como atributo
        self.controlador = AreasController(self)


    def obtener_datos_formulario(self):
        area_nombre = self.ids.area_nombre.text

        # Validación básica
        if not area_nombre:
            self.mostrar_error("El nombre del área es obligatorio.")
            return None

        return {"area": area_nombre}

    def actualizar_lista_areas(self, areas):
        lista_areas_grid = self.ids.lista_areas
        lista_areas_grid.clear_widgets()
        for area in areas:
            lista_areas_grid.add_widget(Label(text=area.nombre))
            lista_areas_grid.add_widget(Button(text="Editar", on_press=lambda btn, id=area.id: self.editar_area(id)))
            lista_areas_grid.add_widget(Button(text="Eliminar", on_press=lambda btn, id=area.id: self.controlador.eliminar_area(id)))

    def editar_area(self, id):
        area = self.controlador.obtener_area(id)
        if area:
            self.ids.area_nombre.text = area.nombre
            self.ids.area_id.text = str(area.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
