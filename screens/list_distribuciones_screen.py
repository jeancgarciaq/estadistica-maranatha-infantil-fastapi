from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from components.styled_popup import StyledPopup
import logging
from kivy.lang import Builder
from datetime import datetime

from components.styled_datepicker import StyledDatePicker

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para mayor detalle
logger = logging.getLogger(__name__)

class ListDistribucionesScreen(Screen):
    """Pantalla para desplegar la lista de distribuciones."""
    def __init__(self, controlador, **kwargs):
        """Inicializando ListDistribucionesScreen."""
        try:
            Builder.load_file("views/list_distribuciones.kv")
        except Exception as e:
            logger.error(f"Error cargando la vista de lista de distribuciones: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializado ListAreasScreen")
        # Asignar el controlador correctamente
        self.controlador = controlador
        self.can_manage = False

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app or not app.can_access_screen('lista_distribuciones'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para ver distribuciones.', tipo='error')
            if app and app.root:
                app.root.current = 'menu'
            return
        self.can_manage = app.has_permission('distribuciones.manage')

    def actualizar_lista_distribuciones(self, distribuciones):
        """Actualiza la lista concentrada para móvil (agrupados + simples)."""
        logger.debug(f"Datos recibidos para actualizar lista de distribuciones: {distribuciones}")
        if not isinstance(distribuciones, list):
            logger.error("El parámetro 'distribuciones' no es una lista. Verifique el controlador.")
            distribuciones = []
        if 'lista_distribuciones' not in self.ids:
            logger.error("No se encontró el id 'lista_distribuciones'. Verifique la estructura de list_distribuciones.kv")
            return
        lista_distribuciones = self.ids.lista_distribuciones
        lista_distribuciones.clear_widgets()

        if not distribuciones or len(distribuciones) == 0:
            lista_distribuciones.add_widget(
                Label(text="No hay distribuciones para la fecha seleccionada", font_size='18sp', size_hint_y=None, height=40)
            )
        else:
            for fila in distribuciones:
                if isinstance(fila, dict) and fila.get('modo') == 'agrupado':
                    lista_distribuciones.add_widget(self._crear_card_agrupada(fila))
                elif isinstance(fila, dict) and fila.get('modo') == 'simple':
                    lista_distribuciones.add_widget(self._crear_card_simple(fila.get('distribucion')))

    def _crear_label(self, **kwargs):
        label = Label(**kwargs)

        def _ajustar_texto(inst, value):
            inst.text_size = (value[0], None)

        label.bind(size=_ajustar_texto)
        return label

    def _crear_card_agrupada(self, fila):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=1,
            height=dp(175),
            padding=dp(10),
            spacing=dp(6),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.2, 0.2, 0.2, 1)
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
        card.bind(pos=lambda w, v: setattr(w._bg, 'pos', v), size=lambda w, v: setattr(w._bg, 'size', v))

        origen_tipo = 'Donación' if fila.get('origen_tipo') == 'donacion' else 'Preparado'
        card.add_widget(self._crear_label(
            text=f"[b]{origen_tipo}: {fila.get('origen_nombre', 'Sin origen')}[/b]",
            markup=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(30),
            font_size='16sp'
        ))
        card.add_widget(self._crear_label(
            text=(
                f"Total: {fila.get('total_cantidad', 0)} {fila.get('unidad', '')} | "
                f"Registros: {fila.get('cantidad_registros', 0)} | "
                f"Destinos: {len(fila.get('destinos', {}))}"
            ),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(48),
            font_size='14sp'
        ))

        acciones = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        btn_detalle = Button(
            text='Ver destinos',
            font_size='13sp',
            background_normal='',
            background_color=(0, 0.47, 0.76, 1),
        )
        btn_detalle.bind(on_release=lambda *_: self._mostrar_detalle_grupo(fila))
        acciones.add_widget(btn_detalle)
        card.add_widget(acciones)
        return card

    def _crear_card_simple(self, distribucion):
        if not distribucion:
            return Label(text='Registro inválido', size_hint_y=None, height=dp(40))

        if getattr(distribucion, 'donacion', None):
            origen_text = f"Donación: {distribucion.donacion.descripcion}"
        elif getattr(distribucion, 'alimento_preparado', None):
            origen_text = f"Preparado: {distribucion.alimento_preparado.descripcion}"
        elif getattr(distribucion, 'donacion_id', None):
            origen_text = f"Donación ID {distribucion.donacion_id}"
        elif getattr(distribucion, 'alimento_preparado_id', None):
            origen_text = f"Preparado ID {distribucion.alimento_preparado_id}"
        else:
            origen_text = 'Sin origen'

        if getattr(distribucion, 'salon', None):
            destino_text = f"Salón: {distribucion.salon.salon}"
        elif getattr(distribucion, 'area', None):
            destino_text = f"Área: {distribucion.area.area}"
        elif getattr(distribucion, 'salon_id', None):
            destino_text = f"Salón ID {distribucion.salon_id}"
        elif getattr(distribucion, 'area_id', None):
            destino_text = f"Área ID {distribucion.area_id}"
        else:
            destino_text = 'Sin destino'

        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=1,
            height=dp(190),
            padding=dp(10),
            spacing=dp(6),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.2, 0.2, 0.2, 1)
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
        card.bind(pos=lambda w, v: setattr(w._bg, 'pos', v), size=lambda w, v: setattr(w._bg, 'size', v))

        card.add_widget(self._crear_label(
            text=f"[b]{origen_text}[/b]",
            markup=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(30),
            font_size='16sp'
        ))
        card.add_widget(self._crear_label(
            text=(
                f"{destino_text}\n"
                f"Cantidad: {distribucion.cantidad} {distribucion.unidad} | Fecha: {distribucion.fecha}"
            ),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(70),
            font_size='14sp'
        ))

        acciones = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        btn_editar = Button(
            text='Editar',
            font_size='13sp',
            background_normal='',
            background_color=(0, 0.5, 1, 1),
            opacity=1 if self.can_manage else 0,
            disabled=not self.can_manage,
        )
        btn_editar.bind(on_release=lambda *_: self.editar_distribucion(distribucion.id))
        btn_borrar = Button(
            text='Eliminar',
            font_size='13sp',
            background_normal='',
            background_color=(1, 0.2, 0.2, 1),
            opacity=1 if self.can_manage else 0,
            disabled=not self.can_manage,
        )
        btn_borrar.bind(on_release=lambda *_: self.confirmar_eliminacion(distribucion.id))
        acciones.add_widget(btn_editar)
        acciones.add_widget(btn_borrar)
        card.add_widget(acciones)
        return card

    def _mostrar_detalle_grupo(self, fila):
        destinos = fila.get('destinos', {})
        if not destinos:
            StyledPopup.mostrar_popup('Detalle', 'Este grupo no tiene destinos para mostrar.', tipo='info')
            return

        layout = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(6))
        grid.bind(minimum_height=grid.setter('height'))

        for destino, cantidad in destinos.items():
            grid.add_widget(self._crear_label(
                text=f"{destino}: {cantidad} {fila.get('unidad', '')}",
                size_hint_y=None,
                height=dp(28),
                halign='left',
                valign='middle',
            ))

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        cerrar = Button(text='Cerrar', size_hint_y=None, height=dp(40))
        layout.add_widget(cerrar)

        popup = Popup(
            title=f"Destinos - {fila.get('origen_nombre', 'Origen')}",
            content=layout,
            size_hint=(0.9, 0.85),
        )
        cerrar.bind(on_release=popup.dismiss)
        popup.open()

    def abrir_datepicker(self, target_id):
        def set_date(date_str):
            self.ids[target_id].text = date_str

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def limpiar_filtro_fecha(self):
        if 'fecha_filtro' in self.ids:
            self.ids.fecha_filtro.text = ''
        self.actualizar_lista_distribuciones([])

    def _obtener_fecha_filtro(self):
        fecha = self.ids.fecha_filtro.text.strip() if 'fecha_filtro' in self.ids else ''
        if not fecha:
            StyledPopup.mostrar_popup('Error', 'Debe seleccionar una fecha para listar las distribuciones.', tipo='error')
            return None

        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup('Error', 'La fecha debe tener el formato YYYY-MM-DD.', tipo='error')
            return None

        return fecha

    def cargar_distribuciones(self):
        """Consulta distribuciones concentradas filtradas por fecha."""
        fecha = self._obtener_fecha_filtro()
        if not fecha:
            return

        try:
            distribuciones = self.controlador.listar_distribuciones_concentradas(fecha)
            if distribuciones is None:
                logger.warning("El método listar_distribuciones_concentradas devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Distribuciones concentradas consultadas: {distribuciones}")
            self.actualizar_lista_distribuciones(distribuciones or [])
        except Exception as e:
            logger.error(f"Error consultando distribuciones: {e}")
            self.actualizar_lista_distribuciones([])

    def on_enter(self, *args):
        """Inicializa la pantalla sin cargar toda la data."""
        if 'fecha_filtro' in self.ids and not self.ids.fecha_filtro.text:
            self.ids.fecha_filtro.text = datetime.now().strftime('%Y-%m-%d')
        self.actualizar_lista_distribuciones([])

    def editar_distribucion(self, dist_id):
        """Navega al formulario para editar la distribución."""
        if not self.can_manage:
            StyledPopup.mostrar_popup('Acceso denegado', 'Solo puede visualizar distribuciones.', tipo='error')
            return
        logger.info(f"Editando distribución ID: {dist_id}")
        dist_screen = self.manager.get_screen('distribuciones')
        dist_screen.preparar_edicion(dist_id)
        self.manager.current = 'distribuciones'

    def confirmar_eliminacion(self, dist_id):
        """Muestra confirmación antes de eliminar."""
        if not self.can_manage:
            StyledPopup.mostrar_popup('Acceso denegado', 'Solo puede visualizar distribuciones.', tipo='error')
            return
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar la distribución ID {dist_id}?",
            on_confirm=lambda: self.eliminar_distribucion(dist_id)
        )

    def eliminar_distribucion(self, dist_id):
        """Elimina la distribución y refresca la lista."""
        exito, mensaje = self.controlador.eliminar_distribucion(dist_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_distribuciones()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def volver(self, instance):
        """Regresa a la pantalla de distribuciones"""
        self.manager.current = 'distribuciones'

