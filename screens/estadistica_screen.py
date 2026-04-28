import logging
from datetime import datetime

import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.app import App

from components.styled_datepicker import StyledDatePicker
from components.styled_popup import StyledPopup
from utils.reporte_estadistico import ReporteEstadisticoService

logger = logging.getLogger(__name__)

class EstadisticaScreen(Screen):
    resumen_texto = StringProperty('Seleccione una fecha y genere el resumen.')
    pdf_texto = StringProperty('El PDF se genera desde la vista Reporte.')

    def __init__(self, **kwargs):
        Builder.load_file('views/estadistica.kv')
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        if not self.ids.fecha_reporte.text:
            self.ids.fecha_reporte.text = datetime.now().strftime('%Y-%m-%d')

    def abrir_datepicker(self, target_id):
        def set_date(date_str):
            self.ids[target_id].text = date_str

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def _obtener_servicio(self):
        app = App.get_running_app()
        if not app or not hasattr(app, 'session'):
            raise RuntimeError('No se encontró una sesión activa de base de datos.')
        return ReporteEstadisticoService(app.session)

    def generar_resumen(self):
        fecha_texto = self.ids.fecha_reporte.text.strip()
        if not fecha_texto:
            StyledPopup.mostrar_popup('Error', 'Debe seleccionar una fecha.', tipo='error')
            return

        try:
            servicio = self._obtener_servicio()
            resumen = servicio.obtener_resumen(fecha_texto)
            self.resumen_texto = servicio.formatear_vista_previa(resumen)
            self.pdf_texto = 'El PDF se genera desde la vista Reporte.'
            StyledPopup.mostrar_popup('Éxito', 'Vista previa generada correctamente.', tipo='success')
        except Exception as e:
            logger.exception('Error al generar resumen')
            StyledPopup.mostrar_popup('Error', f'No se pudo generar el resumen: {e}', tipo='error')

    def ir_a_reporte(self):
        app = App.get_running_app()
        if app and app.root:
            app.root.current = 'reporte'
