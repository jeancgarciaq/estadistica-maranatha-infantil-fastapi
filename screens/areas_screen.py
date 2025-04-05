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
        """Desplegar un popup con el mensaje de error."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)
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
            title_color=(1, 1, 1, 1),
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()
    
    def mostrar_exito(self, mensaje):
        """Display a popup with the area message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)
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
            title="Éxito",
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()
