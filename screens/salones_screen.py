import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from controllers import SalonesController
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import logging

# Configuración de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class SalonesScreen(Screen):
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/salones.kv')
        except Exception as e:
            print(f"Error al cargar salones.kv: {e}")
        super().__init__(**kwargs)
        # Crear el controlador como atributo
        self.controlador = SalonesController(self)
        self.vista = self

    def obtener_datos_formulario(self):
        salon_nombre = self.ids.salon_nombre.text
        salon_edad = self.ids.salon_edad.text

        # Validación básica
        if not salon_nombre:
            self.mostrar_error("El nombre del salón es obligatorio.")
            return None
        if not salon_edad:
            self.mostrar_error("La edad del salón es obligatoria.")
            return None

        return {
            "salon": salon_nombre,
            "edad": salon_edad
        }
    
    def actualizar_lista_salones(self, salones):
        lista_salones_grid = self.ids.lista_salones
        lista_salones_grid.clear_widgets()
        for salon in salones:
            lista_salones_grid.add_widget(Label(text=salon.salon + " (" + salon.edad + ")"))
            lista_salones_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=salon.id: self.editar_salon(id)))
            lista_salones_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=salon.id: self.controlador.eliminar_salon(id)))

    def editar_salon(self, id):
        salon = self.controlador.obtener_salon(id)
        if salon:
            self.ids.salon_salon.text = salon.salon
            self.ids.salon_edad.text = salon.edad
            self.ids.salon_id.text = str(salon.id)

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