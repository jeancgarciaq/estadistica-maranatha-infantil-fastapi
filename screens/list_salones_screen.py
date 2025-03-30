from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListSalonesScreen(Screen):
    """ Pantalla que muestra una lista de salones. """
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_salones.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_salones.kv: {e}")
        super().__init__(**kwargs)
        # Crear el controlador como atributo
        self.controlador = controlador
        logger.info("Initializing ListSalonesScreen")
        self.cargar_salones()

    def on_pre_enter(self):
        self.cargar_salones()

    def cargar_salones(self):
        """Actualiza la lista de salones en la vista"""
        lista_salones_grid = self.ids.lista_salones
        lista_salones_grid.clear_widgets()
        salones = self.controlador.obtener_todos_los_salones()
        if not salones:
            lista_salones_grid.add_widget(Label(text="No hay salones disponibles.", size_hint_y=None, height=40))
        else:
            for salon in salones:
                lista_salones_grid.add_widget(Label(text=f"{salon.salon} ({salon.edad})", size_hint_y=None, height=40))