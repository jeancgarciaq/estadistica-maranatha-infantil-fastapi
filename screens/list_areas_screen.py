import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListAreasScreen(Screen):
    """Pantalla para desplegar la lista de areas."""
    def __init__(self, controlador, vista, **kwargs):
        """Inicializando ListAreasScreen."""
        try:
            Builder.load_file("views/list_areas.kv")
        except Exception as e:
            logger.error(f"Error cargando la vista de áreas: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializado ListAreasScreen")
        # Asignar el controlador correctamente
        self.controlador = controlador  
        self.vista = self

    def actualizar_lista_areas(self, areas):
        """Actualiza la lista de áreas en la vista"""
        logger.debug(f"Datos recibidos para actualizar lista de áreas: {areas}")
        if not isinstance(areas, list):
            logger.error("El parámetro 'areas' no es una lista. Verifique el controlador.")
            areas = []
        lista_areas = self.ids.lista_areas
        lista_areas.clear_widgets()
        if not areas or len(areas) == 0:
            lista_areas.add_widget(Label(text="No hay áreas registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for area in areas:
                logger.debug(f"Agregando área: ID={area.id}, Nombre={area.area}")
                lista_areas.add_widget(Label(text=f"{area.id}", size_hint_y=None, height=40))
                lista_areas.add_widget(Label(text=area.area, size_hint_y=None, height=40))

    def cargar_areas(self):
        """Consultando y llenando la lista areas."""
        try:
            areas = self.controlador.listar_areas(self.vista)
            if areas is None:
                logger.warning("El método listar_areas devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Áreas consultadas: {areas}")
            self.actualizar_lista_areas(areas or [])  # Asegurarse de pasar una lista vacía si es None
        except Exception as e:
            logger.error(f"Error consultando areas: {e}")
            self.actualizar_lista_areas([])

    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_areas()

    def volver(self, instance):
        """Regresa a la pantalla de áreas"""
        self.manager.current = 'areas'

