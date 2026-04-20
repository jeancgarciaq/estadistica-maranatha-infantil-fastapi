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
            color=(1, 1, 1, 1),  # Texto blanco
            halign='center',
            valign='middle'
        )
        popup_label.bind(size=lambda s, w: setattr(popup_label, 'text_size', (w[0], None)))
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
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Evitar que se cierre automáticamente
        )
        popup.content = popup_layout  # Asignar el layout como contenido del popup

        # Vincular el botón "Cerrar" al método dismiss del popup
        close_button.bind(on_release=popup.dismiss)

        # Mostrar el popup
        popup.open()

    @staticmethod
    def mostrar_confirmacion(titulo, mensaje, on_confirm):
        """
        Muestra un popup de confirmación con botones 'Confirmar' y 'Cancelar'.
        :param titulo: Título del popup.
        :param mensaje: Mensaje a mostrar.
        :param on_confirm: Función callback que se ejecuta al confirmar.
        """
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.7),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        popup_label.bind(size=lambda s, w: setattr(popup_label, 'text_size', w))
        popup_layout.add_widget(popup_label)

        # Contenedor para los botones
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.3))
        
        # Botón Cancelar
        cancel_button = Button(
            text="Cancelar",
            background_normal='',
            background_color=(0.5, 0.5, 0.5, 1), # Gris
            height=50
        )
        
        # Botón Confirmar
        confirm_button = Button(
            text="Confirmar",
            background_normal='',
            background_color=(0, 150/255, 0, 1), # Verde oscuro
            height=50
        )
        
        buttons_layout.add_widget(cancel_button)
        buttons_layout.add_widget(confirm_button)
        popup_layout.add_widget(buttons_layout)

        popup = StyledPopup(
            title=titulo,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        popup.content = popup_layout

        # Vincular botones
        cancel_button.bind(on_release=popup.dismiss)
        
        def on_confirm_pressed(instance):
            popup.dismiss()
            on_confirm()
            
        confirm_button.bind(on_release=on_confirm_pressed)

        popup.open()

    def cerrar_popup(self):
        """Cierra el popup actual."""
        self.dismiss()