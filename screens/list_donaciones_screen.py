from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import logging
from datetime import datetime
from components import StyledPopup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Clase ListDonacionScreen
class ListDonacionesScreen(Screen):
    """ Pantalla que muestra una lista de donaciones. """
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_donaciones.kv')
        except Exception as e:
            logger.error(f"Error al cargar vista de lista de donaciones: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializando ListDonacionesScreen")
        self.controlador = controlador
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

                    # Obtener fecha como string de forma robusta
                    fecha_str = ""
                    if hasattr(donacion, 'fecha'):
                        if isinstance(donacion.fecha, str):
                            fecha_str = donacion.fecha
                        elif hasattr(donacion.fecha, 'strftime'):
                            fecha_str = donacion.fecha.strftime('%Y-%m-%d')
                        else:
                            fecha_str = str(donacion.fecha)
                    
                    if not fecha_str:
                        logger.error(f"Donación inválida con ID {donacion.id}: fecha faltante o inválida.")
                        continue

                    # Agregar cada donación a la lista
                    logger.debug(f"Agregando donación: ID={donacion.id}, Descripcion={donacion.descripcion}, Cantidad={donacion.cantidad}, Unidad={donacion.unidad}, Equipo={donacion.equipo}, Fecha={fecha_str}")
                    lista_donaciones.add_widget(Label(text=f"{donacion.id}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.descripcion}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.cantidad}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.unidad}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=f"{donacion.equipo}", size_hint_y=None, height=40))
                    lista_donaciones.add_widget(Label(text=fecha_str, size_hint_y=None, height=40))
            except Exception as e:
                logger.error(f"Error inesperado al procesar las donaciones: {e}")
                StyledPopup.mostrar_popup("Error", "Ocurrió un error inesperado al procesar las donaciones.", tipo="error")

            
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
        """Llamado cuando la pantalla está completa."""
        if not self.controlador:
            logger.error("El controlador no está inicializado. No se pueden listar las donaciones.")
            return
        try:
            self.cargar_donaciones()
        except Exception as e:
            logger.error(f"Error consultando donaciones: {e}")
            self.actualizar_lista_donaciones([])

    def volver(self, instance):
        """Regresa a la pantalla de donaciones"""
        self.manager.current = 'donaciones'
