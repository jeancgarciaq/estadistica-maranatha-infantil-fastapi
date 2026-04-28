from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivy.factory import Factory
from kivy.metrics import dp
from components.styled_popup import StyledPopup
from components.styled_datepicker import StyledDatePicker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
try:
    Builder.load_file('views/list_logisticas.kv')
except Exception as e:
    logger.error(f"Error cargando list_logisticas.kv: {e}")

class ListLogisticaScreen(Screen):
    controlador = ObjectProperty(None)
    fecha_filtro = StringProperty("")

    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador
        logger.info("Inicializando ListLogisticaScreen")

    def on_enter(self, *args):
        if not self.fecha_filtro:
            self.fecha_filtro = datetime.now().strftime('%Y-%m-%d')
        self.actualizar_lista([]) # Iniciar con la lista vacía hasta filtrar

    def abrir_datepicker_filtro(self):
        """Abre el selector de fecha para filtrar registros."""
        def set_date(date_str):
            self.fecha_filtro = date_str
            self.cargar_logisticas()

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def _obtener_fecha_filtro(self):
        """Valida y devuelve la fecha seleccionada para el filtro."""
        fecha = (self.fecha_filtro or "").strip()
        if not fecha:
            StyledPopup.mostrar_popup("Error", "Debe seleccionar una fecha para listar los datos.", tipo="error")
            return None

        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return fecha
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha inválido.", tipo="error")
            return None

    def cargar_logisticas(self):
        fecha = self._obtener_fecha_filtro()
        if not fecha:
            return

        try:
            logisticas = self.controlador.listar_logisticas(fecha=fecha)
            self.actualizar_lista(logisticas)
        except Exception as e:
            logger.error(f"Error al cargar logísticas: {e}")
            self.actualizar_lista([])

    def actualizar_lista(self, logisticas):
        contenedor = self.ids.lista_logisticas
        contenedor.clear_widgets()

        if not logisticas:
            contenedor.add_widget(Label(text='No hay registros de logística para esta fecha.', size_hint_y=None, height=dp(40)))
            return

        for log in logisticas:
            card = Factory.LogisticaCard()
            card.log_id = str(log.id)
            card.capitan = str(log.capitan)
            card.almacen = str(log.almacen)
            card.fecha = log.fecha.strftime('%Y-%m-%d') if log.fecha else ""
            card.distribucion = str(log.distribucion or 'N/A')
            card.hidratacion = str(log.hidratacion or 'N/A')
            card.pasillo = str(log.pasillo or 'N/A')
            card.secretaria = str(log.secretaria or 'N/A')
            
            contenedor.add_widget(card)

    def editar_registro(self, log_id):
        """Redirige a la pantalla de formulario para editar la logística."""
        log_id = int(log_id)
        self.manager.current = 'logisticas'
        logistica_screen = self.manager.get_screen('logisticas')
        logistica_screen.cargar_logistica_para_edicion(log_id)

    def confirmar_eliminacion(self, log_id):
        """Muestra el popup de confirmación antes de borrar."""
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la logística ID {log_id}?",
            on_confirm=lambda: self._ejecutar_eliminacion(int(log_id))
        )

    def _ejecutar_eliminacion(self, log_id):
        exito, mensaje = self.controlador.eliminar_logistica(log_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_logisticas() # Refrescar la lista
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")