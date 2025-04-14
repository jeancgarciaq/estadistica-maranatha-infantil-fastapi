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
class ListDonacionesScreen(Screen):
    """ Pantalla que muestra una lista de donaciones. """
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/list_donaciones.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_donaciones.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Initializando ListDonacionesScreen")
        # Crear el controlador como atributo
        self.controlador = controlador
        self.vista = self  
        

    def actualizar_lista_donaciones(self, donaciones):
        """Actualiza la lista de donaciones en la vista."""
        logger.debug(f"Datos recibidos para actualizar lista de donaciones: {donaciones}")
        if not isinstance(donaciones, list):
            logger.error("El parámetro 'donaciones' no es una lista. Verifique el controlador.")
            donaciones = []
        lista_donaciones = self.ids.lista_donaciones
        lista_donaciones.clear_widgets()
        if not donaciones or len(donaciones) == 0:
            lista_donaciones.add_widget(Label(text="No hay donaciones registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for donacion in donaciones: 
                logger.debug(f"Agregando donaciones: ID={donacion.id}, Descripcion={donacion.descripcion}, Cantidad={donacion.cantidad}, Unidad={donacion.unidad}, Equipo={donacion.equipo}, Fecha={donacion.fecha}")
                lista_donaciones.add_widget(Label(text=f"{donacion.id}", size_hint_y=None, height=40))
                lista_donaciones.add_widget(Label(text=f"{donacion.descripcion}", size_hint_y=None, height=40))
                lista_donaciones.add_widget(Label(text=f"{donacion.cantidad}", size_hint_y=None, height=40))
                lista_donaciones.add_widget(Label(text=f"{donacion.unidad}", size_hint_y=None, height=40))
                lista_donaciones.add_widget(Label(text=f"{donacion.equipo}", size_hint_y=None, height=40))
                lista_donaciones.add_widget(Label(text=f"{donacion.fecha}", size_hint_y=None, height=40))        
            
    def cargar_donaciones(self):
        """Consultando y llenando la lista donaciones."""
        try:
            donaciones = self.controlador.listar_donaciones(self) 
            if donaciones is None:
                logger.warning("El método listar_donaciones devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Donaciones consultadas: {donaciones}")
            self.actualizar_lista_donaciones(donaciones or [])
        except Exception as e:
            logger.error(f"Error consultando donaciones: {e}")
            self.actualizar_lista_donaciones([])
    
    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_donaciones()

    def volver(self, instance):
        """Regresa a la pantalla de donaciones"""
        self.manager.current = 'donaciones'
