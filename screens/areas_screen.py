import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from controllers import AreasController
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class AreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/areas.kv')
        super().__init__(**kwargs)
        self.controlador = AreasController(self)
    
    def obtener_datos_formulario(self):
        area_nombre = self.ids.area_nombre.text

        # Validación básica
        if not area_nombre:
            self.mostrar_error("El nombre del área es obligatorio.")
            return None

        return {
            "area": area_nombre
        }

    def actualizar_lista_areas(self, areas):
        lista_areas_grid = self.ids.lista_areas
        lista_areas_grid.clear_widgets()
        for area in areas:
            lista_areas_grid.add_widget(Label(text=area.nombre))
            lista_areas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=area.id: self.editar_area(id)))
            lista_areas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=area.id: self.controlador.eliminar_area(id)))

    def editar_area(self, id):
        area = self.controlador.obtener_area(id)
        if area:
            self.ids.area_nombre.text = area.nombre
            self.ids.area_id.text = str(area.id)

    def mostrar_popup_lista(self):
        areas = self.controlador.listar_areas()  # Obtener la lista de áreas desde el controlador

        # Crear el contenido del popup (lista de áreas)
        content = ScrollView(
            GridLayout(
                cols=3,
                size_hint_y=None,
                height=self.minimum_height,
                id='lista_areas_popup'  # ID para el GridLayout del popup
            )
        )

        for area in areas:
            content.children[0].add_widget(Label(text=str(area.id)))
            content.children[0].add_widget(Label(text=area.area))  

        # Crear el botón de cerrar
        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        # Crear el popup
        popup = Popup(title='Lista de Áreas', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 400))
        popup.content.add_widget(content)
        popup.content.add_widget(close_button)

        # Asignar la función de cierre al botón
        close_button.bind(on_press=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
