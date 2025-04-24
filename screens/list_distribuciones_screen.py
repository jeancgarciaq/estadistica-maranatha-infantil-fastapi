from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
import logging
from kivy.lang import Builder

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para mayor detalle
logger = logging.getLogger(__name__)

class ListDistribucionesScreen(Screen):
    """Pantalla para desplegar la lista de distribuciones."""
    def __init__(self, controlador, vista, **kwargs):
        """Inicializando ListDistribucionesScreen."""
        try:
            Builder.load_file("views/list_distribuciones.kv")
        except Exception as e:
            logger.error(f"Error cargando la vista de lista de distribuciones: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializado ListAreasScreen")
        # Asignar el controlador correctamente
        self.controlador = controlador  
        self.vista = self

    def actualizar_lista_distribuciones(self, distribuciones):
        """ Actualiza la vista de la lista de las distribuciones """
        logger.debug(f"Datos recibidos para actualizar lista de distribuciones: {distribuciones}")
        if not isinstance(distribuciones, list):
            logger.error("El parámetro 'distribuciones' no es una lista. Verifique el controlador.")
            distribuciones = []
        lista_distribuciones = self.ids.lista_distribuciones
        lista_distribuciones.clear_widgets()
        if not distribuciones or len(distribuciones) == 0:
            lista_distribuciones.add_widget(Label(text="No hay áreas registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for area in distribuciones:
                logger.debug(f"Agregando distribución: ID={distribucion.id}, ID Salón={distribucion.id_salon}, ID Donación={distribucion.id_donacion}, Cantidad={distribucion.cantidad}, Fecha={distribucion.fecha}")
                lista_distribuciones.add_widget(Label(text=f"{distribucion.id}", size_hint_y=None, height=40))
                lista_distribuciones.add_widget(Label(text=distribucion.id_salon, size_hint_y=None, height=40))
                lista_distribuciones.add_widget(Label(text=distribucion.id_donacion, size_hint_y=None, height=40))
                lista_distribuciones.add_widget(Label(text=distribucion.cantidad, size_hint_y=None, height=40))
                lista_distribuciones.add_widget(Label(text=distribucion.fecha, size_hint_y=None, height=40))

    def cargar_distribuciones(self):
        """Consultando y llenando la lista distribuciones."""
        try:
            distribuciones = self.controlador.listar_distribuciones(self.vista)
            if distribuciones is None:
                logger.warning("El método listar_distribuciones devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Distribuciones consultadas: {distribuciones}")
            self.actualizar_lista_distribuciones(distribuciones or [])  # Asegurarse de pasar una lista vacía si es None
        except Exception as e:
            logger.error(f"Error consultando distribuciones: {e}")
            self.actualizar_lista_distribuciones([])

    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_distribuciones()

    def volver(self, instance):
        """Regresa a la pantalla de áreas"""
        self.manager.current = 'distribuciones'

