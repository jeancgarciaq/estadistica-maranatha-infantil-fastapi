from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Modificando
class ListSalonesScreen(Screen):
    """ Pantalla que muestra una lista de salones. """
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/list_salones.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_salones.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Initializando ListSalonesScreen")
        # Crear el controlador como atributo
        self.controlador = controlador
        self.vista = self  
        

    def actualizar_lista_salones(self, salones):
        """Actualiza la lista de salones en la vista."""
        logger.debug(f"Datos recibidos para actualizar lista de salones: {salones}")
        if not isinstance(salones, list):
            logger.error("El parámetro 'salones' no es una lista. Verifique el controlador.")
            salones = []
        lista_salones = self.ids.lista_salones
        lista_salones.clear_widgets()
        if not salones or len(salones) == 0:
            lista_salones.add_widget(Label(text="No hay salones registrados", font_size='18sp', size_hint_y=None, height=40))
        else:
            for salon in salones:
                logger.debug(f"Agregando salón: ID={salon.id}, Nombre={salon.salon}, Edad={salon.edad}")
                lista_salones.add_widget(Label(text=f"{salon.id}", size_hint_y=None, height=40))
                lista_salones.add_widget(Label(text=salon.salon, size_hint_y=None, height=40))
                lista_salones.add_widget(Label(text=salon.edad, size_hint_y=None, height=40))
            
    def cargar_salones(self):
        """Consultando y llenando la lista salones."""
        try:
            salones = self.controlador.listar_salones(self)  # Pasa 'self' como vista
            if salones is None:
                logger.warning("El método listar_salones devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Salones consultados: {salones}")
            self.actualizar_lista_salones(salones or [])
        except Exception as e:
            logger.error(f"Error consultando salones: {e}")
            self.actualizar_lista_salones([])
    
    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_salones()

    def volver(self, instance):
        """Regresa a la pantalla de salones"""
        self.manager.current = 'salones'


