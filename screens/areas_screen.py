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
from components.styled_popup import StyledPopup
from controllers import AreasController
import logging


# Configuración de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class AreasScreen(Screen):
    def __init__(self, controlador, vista, **kwargs):
        # Cargar el archivo KV dentro del try-except
        try:
            Builder.load_file('views/areas.kv')
        except Exception as e:
            print(f"Error al cargar areas.kv: {e}")
        super().__init__(**kwargs)
        # Pass 'self' as the 'vista' to the controller
        self.controlador = AreasController(self)
        self.vista = self


    def obtener_datos_formulario(self):
        area_nombre = self.ids.area_nombre.text

        # Validación básica
        if not area_nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del área es obligatorio.", tipo="error")
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

    def buscar_area(self):
        """Obtiene los datos del formulario y llama al método buscar_area del controlador."""
        area_id = self.ids.area_id.text.strip()  # ID del área
        area_nombre = self.ids.area_nombre.text.strip()  # Nombre del área

        # Validar que al menos uno de los campos esté lleno
        if not area_id and not area_nombre:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o un nombre para buscar el área.", tipo="error")
            return

        # Convertir el ID a entero si es posible
        area_id = int(area_id) if area_id.isdigit() else None

        # Llamar al método buscar_area del controlador
        self.controlador.buscar_area(id=area_id, nombre=area_nombre)