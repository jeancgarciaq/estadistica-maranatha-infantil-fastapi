import os
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
    pdf_texto = StringProperty('')

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
            graficos = servicio.generar_graficos(resumen)
            pdf = servicio.generar_pdf(resumen, graficos)

            self.resumen_texto = (
                f'Fecha: {resumen.fecha_corte.strftime("%d/%m/%Y")}\n'
                f'Total asistencia: {resumen.total_asistencia}\n'
                f'Niños: {resumen.asistencia_ninos} | Niñas: {resumen.asistencia_ninas} | Servidores: {resumen.asistencia_servidores}\n'
                f'Preparado: {resumen.donaciones_combinadas:.2f}\n'
                f'Distribuido: {resumen.distribuciones_combinadas:.2f}\n'
                f'Pendiente: {resumen.faltante_preparado:.2f}\n'
                f'¿Se repartió todo?: {"Sí" if resumen.preparacion_completa else "No"}'
            )
            self.pdf_texto = f'PDF generado en: {pdf}'
            self._ultimo_pdf = pdf
            StyledPopup.mostrar_popup('Éxito', 'Resumen generado correctamente.', tipo='success')
        except Exception as e:
            logger.exception('Error al generar resumen')
            StyledPopup.mostrar_popup('Error', f'No se pudo generar el resumen: {e}', tipo='error')

    def abrir_pdf(self):
        pdf = getattr(self, '_ultimo_pdf', None)
        if not pdf or not os.path.exists(pdf):
            StyledPopup.mostrar_popup('Aviso', 'Primero debe generar el PDF.', tipo='info')
            return
        try:
            os.startfile(pdf)
        except Exception as e:
            StyledPopup.mostrar_popup('Error', f'No se pudo abrir el PDF: {e}', tipo='error')
