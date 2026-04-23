from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import StringProperty
import logging
from datetime import datetime
from components import StyledPopup
from components.styled_datepicker import StyledDatePicker

from kivy.factory import Factory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Clase ListDonacionScreen
class ListDonacionesScreen(Screen):
    """ Pantalla que muestra una lista de donaciones. """
    fecha_filtro = StringProperty("")

    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_donaciones.kv')
        except Exception as e:
            logger.error(f"Error al cargar vista de lista de donaciones: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializando ListDonacionesScreen")
        self.controlador = controlador

    def abrir_datepicker_filtro(self):
        """Abre el selector de fecha para filtrar donaciones."""
        def set_date(date_str):
            self.fecha_filtro = date_str

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def _obtener_fecha_filtro(self):
        """Valida y devuelve la fecha seleccionada para el filtro."""
        fecha = (self.fecha_filtro or "").strip()
        if not fecha:
            StyledPopup.mostrar_popup("Error", "Debe seleccionar una fecha para listar las donaciones.", tipo="error")
            return None

        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return fecha
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha inválido. Use YYYY-MM-DD.", tipo="error")
            return None

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

                    # Agregar cada donación a la lista usando la nueva tarjeta
                    logger.debug(f"Agregando donación: ID={donacion.id}, Descripcion={donacion.descripcion}, Cantidad={donacion.cantidad}, Unidad={donacion.unidad}, Equipo={donacion.equipo}, Fecha={fecha_str}")
                    
                    card = Factory.DonacionCard()
                    card.donacion_id = str(donacion.id)
                    card.descripcion = str(donacion.descripcion)
                    card.cantidad = str(donacion.cantidad)
                    card.unidad = str(donacion.unidad)
                    card.equipo = str(donacion.equipo)
                    card.fecha = fecha_str
                    card.es_compuesta = bool(getattr(donacion, 'es_compuesta', False))
                    
                    lista_donaciones.add_widget(card)
            except Exception as e:
                logger.error(f"Error inesperado al procesar las donaciones: {e}")
                StyledPopup.mostrar_popup("Error", "Ocurrió un error inesperado al procesar las donaciones.", tipo="error")

            
    def cargar_donaciones(self):
        """Consultando y llenando la lista donaciones."""
        if not self.controlador:
            logger.error("El controlador no está inicializado. No se pueden listar las donaciones.")
            return

        fecha = self._obtener_fecha_filtro()
        if not fecha:
            return

        try:
            donaciones = self.controlador.listar_donaciones(fecha=fecha)
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
            # Inicializar filtro con la fecha actual para mantener el flujo de trabajo por día.
            if not self.fecha_filtro:
                self.fecha_filtro = datetime.now().strftime('%Y-%m-%d')
            self.cargar_donaciones()
        except Exception as e:
            logger.error(f"Error consultando donaciones: {e}")
            self.actualizar_lista_donaciones([])

    def volver(self, instance):
        """Regresa a la pantalla de donaciones"""
        self.manager.current = 'donaciones'

    def editar_donacion(self, id_donacion):
        """Regresa a la pantalla de donaciones y carga los datos para editar."""
        logger.info(f"Editando donación con ID: {id_donacion}")
        self.manager.current = 'donaciones'
        donaciones_screen = self.manager.get_screen('donaciones')
        donaciones_screen.editar_donacion(int(id_donacion))

    def confirmar_eliminacion(self, id_donacion):
        """Muestra el popup de confirmación antes de eliminar."""
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            "Esta acción no se puede deshacer. ¿Está seguro de que desea eliminar este registro?",
            on_confirm=lambda: self.eliminar_donacion(id_donacion)
        )

    def eliminar_donacion(self, id_donacion):
        """Ejecuta la eliminación de la donación."""
        logger.info(f"Eliminando donación con ID: {id_donacion}")
        exito, mensaje = self.controlador.eliminar_donacion(int(id_donacion))
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_donaciones() # Actualizar la lista
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")
