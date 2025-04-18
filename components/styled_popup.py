from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Cargar el archivo popup.kv
Builder.load_file('views/popup.kv')

class StyledPopup(Popup):
    """Clase para el diseño del popup reutilizable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def mostrar_popup(titulo, mensaje, tipo="info"):
        """
        Muestra un popup con un mensaje.
        :param titulo: Título del popup.
        :param mensaje: Mensaje a mostrar en el popup.
        :param tipo: Tipo de mensaje ('info', 'error', 'success').
        """
        # Definir colores según el tipo de mensaje
        colores = {
            "info": (0, 119/255, 194/255, 1),  # Azul
            "error": (1, 0, 0, 1),  # Rojo
            "success": (0, 1, 0, 1)  # Verde
        }
        color = colores.get(tipo, (0, 119/255, 194/255, 1))  # Azul por defecto

        # Crear el contenido del popup
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)  # Texto blanco
        )
        popup_layout.add_widget(popup_label)

        # Botón "Cerrar"
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            background_normal='',
            background_color=color,  # Color según el tipo de mensaje
            height=50
        )
        popup_layout.add_widget(close_button)

        # Crear el popup
        popup = StyledPopup(
            title=titulo,
            content=popup_layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Evitar que se cierre automáticamente
        )

        # Vincular el botón "Cerrar" al método dismiss del popup
        close_button.bind(on_release=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def cerrar_popup(self):
        """Cierra el popup actual."""
        self.dismiss()