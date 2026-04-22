import logging
from datetime import datetime

import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from components.styled_datepicker import StyledDatePicker
from components.styled_popup import StyledPopup

logger = logging.getLogger(__name__)

class EstadisticaScreen(Screen):
    resumen_texto = StringProperty('Seleccione una fecha para cargar el informe.')

    def __init__(self, controlador=None, **kwargs):
        self.controlador = controlador
        self._ultimo_resumen = None
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
        if self.controlador is not None:
            return self.controlador
        controlador = getattr(app, 'estadistica_controller', None)
        if controlador is None:
            raise RuntimeError('No se encontró un controlador de estadística activo.')
        return controlador

    def actualizar_vista(self):
        fecha_texto = self.ids.fecha_reporte.text.strip()
        if not fecha_texto:
            StyledPopup.mostrar_popup('Error', 'Debe seleccionar una fecha.', tipo='error')
            return

        try:
            controlador = self._obtener_servicio()
            informe = controlador.obtener_vista_estadistica(fecha_texto)
            resumen = informe['resumen']

            self._renderizar_informe(informe)

            self.resumen_texto = f'Vista del informe cargada para {resumen.fecha_corte.strftime("%d/%m/%Y")}.'
            self._ultimo_resumen = resumen
            StyledPopup.mostrar_popup('Éxito', 'Vista de estadística actualizada correctamente.', tipo='success')
        except Exception as e:
            logger.exception('Error al actualizar vista de estadística')
            StyledPopup.mostrar_popup('Error', f'No se pudo actualizar la vista: {e}', tipo='error')

    def _renderizar_informe(self, informe):
        contenedor = self.ids.informe_container
        contenedor.clear_widgets()

        for seccion in informe['secciones']:
            if seccion['tipo'] == 'texto':
                if seccion.get('titulo'):
                    contenedor.add_widget(self._crear_titulo(seccion['titulo']))
                contenedor.add_widget(self._crear_parrafo(seccion['texto']))
            elif seccion['tipo'] == 'tabla':
                contenedor.add_widget(self._crear_bloque_tabla(
                    seccion.get('titulo'),
                    seccion['encabezados'],
                    seccion['filas']
                ))
            elif seccion['tipo'] == 'imagen':
                if seccion.get('titulo'):
                    contenedor.add_widget(self._crear_titulo(seccion['titulo']))
                contenedor.add_widget(Image(
                    source=seccion['ruta'],
                    size_hint_y=None,
                    height=280,
                    allow_stretch=True,
                    keep_ratio=True,
                ))

    def _crear_titulo(self, texto):
        etiqueta = Label(
            text=f'[b]{texto}[/b]',
            markup=True,
            color=(1, 1, 1, 1),
            font_size=18,
            size_hint_y=None,
            halign='left',
            valign='middle',
        )
        etiqueta.bind(size=lambda instancia, valor: setattr(instancia, 'text_size', (valor[0], None)))
        etiqueta.bind(texture_size=lambda instancia, valor: setattr(instancia, 'height', valor[1] + 10))
        return etiqueta

    def _crear_parrafo(self, texto):
        etiqueta = Label(
            text=texto,
            color=(1, 1, 1, 1),
            font_size=15,
            size_hint_y=None,
            halign='left',
            valign='top',
        )
        etiqueta.bind(size=lambda instancia, valor: setattr(instancia, 'text_size', (valor[0], None)))
        etiqueta.bind(texture_size=lambda instancia, valor: setattr(instancia, 'height', valor[1] + 10))
        return etiqueta

    def _crear_bloque_tabla(self, titulo, encabezados, filas):
        bloque = GridLayout(cols=1, size_hint_y=None, spacing=6)
        bloque.bind(minimum_height=bloque.setter('height'))

        if titulo:
            bloque.add_widget(self._crear_titulo(titulo))

        tabla = GridLayout(
            cols=len(encabezados),
            size_hint_y=None,
            spacing=1,
            row_default_height=40,
            row_force_default=True,
        )
        tabla.height = 40 * (len(filas) + 1) + max(len(filas), 0)

        for encabezado in encabezados:
            tabla.add_widget(self._crear_celda(encabezado, encabezado=True))

        for indice, fila in enumerate(filas):
            for celda in fila:
                tabla.add_widget(self._crear_celda(celda, encabezado=False, alternado=indice % 2 == 1))

        bloque.add_widget(tabla)
        return bloque

    def _crear_celda(self, texto, encabezado=False, alternado=False):
        if encabezado:
            color_fondo = (0.10, 0.20, 0.36, 1)
            color_texto = (1, 1, 1, 1)
        else:
            color_fondo = (0.94, 0.95, 0.97, 1) if alternado else (0.88, 0.90, 0.94, 1)
            color_texto = (0.12, 0.12, 0.12, 1)

        celda = BoxLayout(size_hint_y=None, height=40, padding=[6, 4, 6, 4])
        with celda.canvas.before:
            Color(*color_fondo)
            rectangulo = Rectangle(pos=celda.pos, size=celda.size)

        def actualizar_rectangulo(*_):
            rectangulo.pos = celda.pos
            rectangulo.size = celda.size

        celda.bind(pos=actualizar_rectangulo, size=actualizar_rectangulo)

        etiqueta = Label(
            text=str(texto),
            color=color_texto,
            font_size=13,
            halign='center',
            valign='middle',
        )
        etiqueta.bind(size=lambda instancia, valor: setattr(instancia, 'text_size', (valor[0] - 12, None)))
        celda.add_widget(etiqueta)
        return celda

