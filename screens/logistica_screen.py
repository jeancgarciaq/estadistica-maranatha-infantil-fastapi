from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from components.styled_popup import StyledPopup
from components.styled_datepicker import StyledDatePicker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
try:
    Builder.load_file('views/logistica.kv')
except Exception as e:
    logger.error(f"Error cargando logistica.kv: {e}")

class LogisticaScreen(Screen):
    controlador = ObjectProperty(None)
    
    # Propiedades para el formulario
    logistica_id_text = StringProperty('')
    logistica_almacen_text = StringProperty('')
    logistica_capitan_text = StringProperty('')
    logistica_distribucion_text = StringProperty('')
    logistica_hidratacion_text = StringProperty('')
    logistica_pasillo_text = StringProperty('')
    logistica_secretaria_text = StringProperty('')
    logistica_fecha_text = StringProperty(datetime.now().strftime('%Y-%m-%d'))

    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador
        logger.info("Inicializando LogisticaScreen")

    def on_enter(self, *args):
        # Limpiar el formulario al entrar a la pantalla
        self.limpiar_formulario()
        self.logistica_fecha_text = datetime.now().strftime('%Y-%m-%d')

    def abrir_datepicker(self, target_id):
        """Abre el selector de fecha para el campo de fecha."""
        def set_date(date_str):
            if target_id == 'logistica_fecha':
                self.logistica_fecha_text = date_str
            # Add other date fields if any

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def limpiar_formulario(self):
        self.logistica_id_text = ''
        self.logistica_almacen_text = ''
        self.logistica_capitan_text = ''
        self.logistica_distribucion_text = ''
        self.logistica_hidratacion_text = ''
        self.logistica_pasillo_text = ''
        self.logistica_secretaria_text = ''
        self.logistica_fecha_text = datetime.now().strftime('%Y-%m-%d')

    def _obtener_datos_formulario(self):
        datos = {
            'almacen': self.ids.logistica_almacen.text.strip() if 'logistica_almacen' in self.ids else self.logistica_almacen_text.strip(),
            'capitan': self.ids.logistica_capitan.text.strip() if 'logistica_capitan' in self.ids else self.logistica_capitan_text.strip(),
            'distribucion': self.ids.logistica_distribucion.text.strip() if 'logistica_distribucion' in self.ids else self.logistica_distribucion_text.strip(),
            'hidratacion': self.ids.logistica_hidratacion.text.strip() if 'logistica_hidratacion' in self.ids else self.logistica_hidratacion_text.strip(),
            'pasillo': self.ids.logistica_pasillo.text.strip() if 'logistica_pasillo' in self.ids else self.logistica_pasillo_text.strip(),
            'secretaria': self.ids.logistica_secretaria.text.strip() if 'logistica_secretaria' in self.ids else self.logistica_secretaria_text.strip(),
            'fecha': self.ids.logistica_fecha.text.strip() if 'logistica_fecha' in self.ids else self.logistica_fecha_text.strip()
        }
        return datos

    def crear_logistica(self):
        datos = self._obtener_datos_formulario()
        exito, mensaje = self.controlador.crear_logistica(datos)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_logistica(self):
        log_id_str = self.logistica_id_text.strip()
        if not log_id_str:
            StyledPopup.mostrar_popup("Error", "Debe ingresar un ID de logística para actualizar.", tipo="error")
            return
        try:
            log_id = int(log_id_str)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "El ID de logística debe ser un número entero.", tipo="error")
            return

        datos = self._obtener_datos_formulario()
        exito, mensaje = self.controlador.actualizar_logistica(log_id, datos)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_logistica(self, log_id_str):
        if not log_id_str:
            StyledPopup.mostrar_popup("Error", "Debe ingresar un ID de logística para eliminar.", tipo="error")
            return
        try:
            log_id = int(log_id_str)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "El ID de logística debe ser un número entero.", tipo="error")
            return

        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la logística ID {log_id}?",
            on_confirm=lambda: self._ejecutar_eliminacion(log_id)
        )

    def _ejecutar_eliminacion(self, log_id):
        exito, mensaje = self.controlador.eliminar_logistica(log_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def cargar_logistica_para_edicion(self, log_id):
        """Carga los datos de una logística en el formulario para su edición."""
        logistica = self.controlador.obtener_logistica(log_id)
        if logistica:
            self.logistica_id_text = str(logistica.id)
            self.logistica_almacen_text = logistica.almacen
            self.logistica_capitan_text = logistica.capitan
            self.logistica_distribucion_text = logistica.distribucion or ''
            self.logistica_hidratacion_text = logistica.hidratacion or ''
            self.logistica_pasillo_text = logistica.pasillo or ''
            self.logistica_secretaria_text = logistica.secretaria or ''
            self.logistica_fecha_text = logistica.fecha.strftime('%Y-%m-%d')
        else:
            StyledPopup.mostrar_popup("Error", "Logística no encontrada para edición.", tipo="error")

    def ir_a_lista_logisticas(self):
        """Navega a la lista, validando primero si la pantalla existe en el manager."""
        if self.manager.has_screen('lista_logisticas'):
            self.manager.current = 'lista_logisticas'
        else:
            logger.error("La pantalla 'lista_logisticas' no ha sido registrada en el ScreenManager.")
            StyledPopup.mostrar_popup("Error", "La vista de listado no está registrada en el sistema.", tipo="error")