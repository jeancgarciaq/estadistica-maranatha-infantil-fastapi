import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListAreasScreen(Screen):
    """Screen for displaying the list of areas."""
        
    def __init__(self, controlador, **kwargs):
        Builder.load_file("views/list_areas.kv")  # Cargar el archivo KV
        super().__init__(**kwargs)
        logger.info("Initializing ListAreasScreen")
        self.controlador = controlador  # Asignar el controlador correctamente

    def actualizar_lista_areas(self, areas):
        """Actualiza la lista de áreas en la vista"""
        lista_areas = self.ids.lista_areas  # Acceder al GridLayout por su ID
        lista_areas.clear_widgets()  # Limpiar widgets previos
        if not areas:
            lista_areas.add_widget(Label(text="No hay áreas registradas", font_size='18sp'))
        else:
            for area in areas:
                lista_areas.add_widget(Label(text=f"{area.id}", size_hint_y=None, height=40))
                lista_areas.add_widget(Label(text=area.area, size_hint_y=None, height=40))

    def volver(self, instance):
        """Regresa a la pantalla de áreas"""
        self.manager.current = 'areas'

