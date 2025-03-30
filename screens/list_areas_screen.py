import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label  # Add this import

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListAreasScreen(Screen):
    """Pantalla para desplegar la lista de areas."""
        
    def __init__(self, controlador, **kwargs):
        """Inicializando ListAreasScreen."""
        try:
            Builder.load_file("views/list_areas.kv")  # Load the KV file
        except Exception as e:
            logger.error(f"Error cargando list_areas.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializado ListAreasScreen")
        # Asignar el controlador correctamente
        self.controlador = controlador  

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

    def cargar_areas(self):
        """Consultando y llenando la lista areas."""
        try:
            areas = self.controlador.obtener_areas()
            self.actualizar_lista_areas(areas)
        except Exception as e:
            logger.error(f"Error consultando areas: {e}")
            self.actualizar_lista_areas([])

    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_areas()

    def volver(self, instance):
        """Regresa a la pantalla de áreas"""
        self.manager.current = 'areas'

