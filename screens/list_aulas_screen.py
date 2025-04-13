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
class ListAulasScreen(Screen):
    """ Pantalla que muestra una lista de aulas. """
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/list_aulas.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_aulas.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Initializando ListAulasScreen")
        # Crear el controlador como atributo
        self.controlador = controlador
        self.vista = self  
        

    def actualizar_lista_aulas(self, aulas):
        """Actualiza la lista de aulas en la vista."""
        logger.debug(f"Datos recibidos para actualizar lista de aulas: {aulas}")
        if not isinstance(aulas, list):
            logger.error("El parámetro 'aulas' no es una lista. Verifique el controlador.")
            aulas = []
        lista_aulas = self.ids.lista_aulas
        lista_aulas.clear_widgets()
        if not aulas or len(aulas) == 0:
            lista_aulas.add_widget(Label(text="No hay aulas registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for aula in aulas: 
                logger.debug(f"Agregando aula: ID={aula.id}, Auxiliar={aula.auxiliar}, Capitan={aula.capitan}, Colaborador={aula.colaborador}, Condición={aula.condicion}, Edad={aula.edad}, Maestra={aula.maestra}, Niños={aula.ninos}, Niñas={aula.ninas}, Subcapitan={aula.subcapitan}, Fecha={aula.fecha}")
                lista_aulas.add_widget(Label(text=f"{aula.id}", size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.capitan, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.colaborador, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.condicion, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.edad, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.maestra, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.ninos, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.ninas, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.subcapitan, size_hint_y=None, height=40))
                lista_aulas.add_widget(Label(text=aula.fecha, size_hint_y=None, height=40))
            
    def cargar_aulas(self):
        """Consultando y llenando la lista aulas."""
        try:
            aulas = self.controlador.listar_aulas(self) 
            if aulas is None:
                logger.warning("El método listar_aulas devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Aulas consultadas: {aulas}")
            self.actualizar_lista_aulas(aulas or [])
        except Exception as e:
            logger.error(f"Error consultando aulas: {e}")
            self.actualizar_lista_aulas([])
    
    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_aulas()

    def volver(self, instance):
        """Regresa a la pantalla de aulas"""
        self.manager.current = 'aulas'


