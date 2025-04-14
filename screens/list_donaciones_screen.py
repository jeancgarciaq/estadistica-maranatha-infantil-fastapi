from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from controllers.donaciones_controller import DonacionesController
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Clase ListDonacionScreen
class ListDonacionesScreen(Screen):
    """ Pantalla que muestra una lista de donaciones. """
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/list_donaciones.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_donaciones.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializando ListDonacionesScreen")
        self.controlador = DonacionesController(self)
        self.vista = self  
        

    def actualizar_lista_donaciones(self, donaciones):
        """Actualiza la lista de donaciones en la vista."""
        logger.debug(f"Datos recibidos para actualizar lista de donaciones: {donaciones}")
        if not hasattr(self.ids, 'lista_donaciones'):
            logger.error("El widget 'lista_donaciones' no está definido en el archivo .kv.")
            return
        if not isinstance(donaciones, list):
            logger.error("El parámetro 'donaciones' no es una lista. Verifique el controlador.")
            donaciones = []
        lista_donaciones = self.ids.lista_donaciones
        lista_donaciones.clear_widgets()
        if not donaciones or all(donacion is None for donacion in donaciones):
            logger.warning("La lista de donaciones está vacía o contiene elementos nulos.")
            lista_donaciones.add_widget(Label(text="No hay donaciones registradas", font_size='18sp', size_hint_y=None, height=40))
            return
        if not donaciones or len(donaciones) == 0:
            lista_donaciones.add_widget(Label(text="No hay donaciones registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            ids = set()
            try:
                for donacion in donaciones:
                    if donacion.id in ids:
                        logger.warning(f"Donación duplicada encontrada con ID {donacion.id}.")
                        continue
                    ids.add(donacion.id)
                    if hasattr(donacion, 'cantidad') and (not isinstance(donacion.cantidad, (int, float)) or donacion.cantidad <= 0):
                        logger.error(f"Cantidad inválida para la donación con ID {donacion.id}: {donacion.cantidad}")
                        continue
                    try:
                        datetime.strptime(donacion.fecha, '%Y-%m-%d')
                    except ValueError:
                        logger.error(f"Formato de fecha inválido para la donación con ID {donacion.id}: {donacion.fecha}")
                        continue
                    if not hasattr(donacion, 'id') or not isinstance(donacion.id, int):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'id' es obligatorio y debe ser un entero.")
                        continue
                    if not hasattr(donacion, 'descripcion') or not isinstance(donacion.descripcion, str):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'descripcion' es obligatorio y debe ser una cadena.")
                        continue
                    if not hasattr(donacion, 'cantidad') or not isinstance(donacion.cantidad, (int, float)):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'cantidad' es obligatorio y debe ser un número.")
                        continue
                    if not hasattr(donacion, 'unidad') or not isinstance(donacion.unidad, str):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'unidad' es obligatorio y debe ser una cadena.")
                        continue
                    if not hasattr(donacion, 'equipo') or not isinstance(donacion.equipo, str):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'equipo' es obligatorio y debe ser una cadena.")
                        continue
                    if not hasattr(donacion, 'fecha') or not isinstance(donacion.fecha, str):
                        logger.error(f"Donación inválida: {donacion}. El atributo 'fecha' es obligatorio y debe ser una cadena.")
                        continue
                    # Agregar cada donación a la lista
                    logger.debug(f"Agregando donación: ID={donacion.id}, Descripcion={donacion.descripcion}, Cantidad={donacion.cantidad}, Unidad={donacion.unidad}, Equipo={donacion.equipo}, Fecha={donacion.fecha}")
                    lista_donaciones.add_widget(Label(text=f"{donacion.id}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.descripcion}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.cantidad}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.unidad}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.equipo}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.fecha}", size_hint_y=None, height=40))
            except Exception as e:
                logger.error(f"Error inesperado al procesar las donaciones: {e}")
                self.mostrar_error("Ocurrió un error al procesar las donaciones. Inténtalo de nuevo.")
            
    def cargar_donaciones(self):
        """Consultando y llenando la lista donaciones."""
        if not self.controlador:
            logger.error("El controlador no está inicializado. No se pueden listar las donaciones.")
            return
        try:
            donaciones = self.controlador.listar_donaciones()
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
