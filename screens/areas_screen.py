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

    def mostrar_popup_lista(self):
        areas = self.controlador.obtener_todas_las_areas()  # Nueva función en el controlador que retorna la lista de áreas

        # Crear el layout para la lista
        lista_areas_popup = GridLayout(cols=2, size_hint_y=None)
        lista_areas_popup.bind(minimum_height=lista_areas_popup.setter('height'))

        for area in areas:
            lista_areas_popup.add_widget(Label(text=str(area.id)))
            lista_areas_popup.add_widget(Label(text=area.nombre))

        # Crear el ScrollView para la lista
        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(lista_areas_popup)

        # Crear el botón de cerrar
        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        # Crear el popup
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(scrollview)
        popup_content.add_widget(close_button)

        popup = Popup(title='Lista de Áreas', content=popup_content, size_hint=(None, None), size=(400, 400))

        # Asignar la función de cierre al botón
        close_button.bind(on_press=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
