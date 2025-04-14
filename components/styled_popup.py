from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Cargar el archivo popup.kv
Builder.load_file('views/popup.kv')

class StyledPopup(BoxLayout):
    """Clase para el diseño del popup reutilizable."""
    pass
