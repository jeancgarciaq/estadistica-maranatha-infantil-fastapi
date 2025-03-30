import logging
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar el archivo KV una sola vez
Builder.load_file("views/list_areas.kv")

class ListAreasScreen(Screen):
    """Screen for displaying the list of areas."""
        
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        logger.info("Initializing ListAreasScreen")
        self.controlador = controlador  # Asignar el controlador correctamente
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title = Label(text="Lista de Áreas", size_hint=(1, 0.1), font_size='20sp', bold=True)
        self.layout.add_widget(self.title)

        # Contenedor para la lista de áreas
        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.areas_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.areas_container.bind(minimum_height=self.areas_container.setter('height'))
        self.scrollview.add_widget(self.areas_container)
        self.layout.add_widget(self.scrollview)

        # Botón para regresar
        self.btn_back = Button(text="Volver", size_hint=(1, 0.1))
        self.btn_back.bind(on_press=self.volver)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def actualizar_lista_areas(self, areas):
        """Actualiza la lista de áreas en la vista"""
        self.ids.lista_areas.clear_widgets()  # Usar el ID definido en el archivo KV
        if not areas:
            self.ids.lista_areas.add_widget(Label(text="No hay áreas registradas", font_size='18sp'))
        else:
            for area in areas:
                self.ids.lista_areas.add_widget(Label(text=f"{area.id}", size_hint_y=None, height=40))
                self.ids.lista_areas.add_widget(Label(text=area.area, size_hint_y=None, height=40))

    def volver(self, instance):
        """Regresa a la pantalla de áreas"""
        self.manager.current = 'areas'

# Initialize ScreenManager and add ListAreasScreen
screen_manager = ScreenManager()
list_areas_screen = ListAreasScreen(controlador=None)
screen_manager.add_widget(list_areas_screen)

