from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import logging

from components.styled_popup import StyledPopup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ListPreparadosScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_preparados.kv')
        except Exception as e:
            logger.error(f"Error cargando list_preparados.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def on_enter(self):
        self.cargar_preparados()

    def cargar_preparados(self):
        preparados = self.controlador.listar_preparados()
        self.actualizar_lista(preparados)

    def actualizar_lista(self, preparados):
        contenedor = self.ids.lista_preparados
        contenedor.clear_widgets()

        if not preparados:
            contenedor.add_widget(Label(text='No hay alimentos preparados registrados.', size_hint_y=None, height=40))
            return

        for preparado in preparados:
            tarjeta = BoxLayout(orientation='vertical', size_hint_y=None, height=170, padding=10, spacing=6)
            tarjeta.add_widget(Label(
                text=f"ID {preparado.id} | {preparado.descripcion}",
                bold=True,
                size_hint_y=None,
                height=28,
                halign='left',
                text_size=(900, None)
            ))
            tarjeta.add_widget(Label(
                text=f"Cantidad: {preparado.cantidad} {preparado.unidad} | Equipo: {preparado.equipo} | Fecha: {preparado.fecha}",
                size_hint_y=None,
                height=24,
                halign='left',
                text_size=(900, None)
            ))

            if preparado.componentes:
                detalle = ', '.join(
                    f"{c.materia_prima.descripcion if c.materia_prima else c.donacion_materia_id}: {c.cantidad_usada}"
                    for c in preparado.componentes
                )
            else:
                detalle = 'Sin componentes registrados'

            tarjeta.add_widget(Label(
                text=f"Materias primas usadas: {detalle}",
                size_hint_y=None,
                height=56,
                halign='left',
                valign='top',
                text_size=(900, None)
            ))

            acciones = BoxLayout(size_hint_y=None, height=34, spacing=8)
            boton = Button(text='Eliminar', background_normal='', background_color=(180/255, 0, 0, 1))
            boton.bind(on_release=lambda btn, p_id=preparado.id: self.confirmar_eliminacion(p_id))
            acciones.add_widget(boton)
            tarjeta.add_widget(acciones)

            contenedor.add_widget(tarjeta)

    def confirmar_eliminacion(self, preparado_id):
        StyledPopup.mostrar_confirmacion(
            'Confirmar Eliminación',
            f'¿Desea eliminar el preparado ID {preparado_id}?',
            on_confirm=lambda: self.eliminar_preparado(preparado_id)
        )

    def eliminar_preparado(self, preparado_id):
        exito, mensaje = self.controlador.eliminar_preparado(preparado_id)
        if exito:
            StyledPopup.mostrar_popup('Éxito', mensaje, tipo='success')
            self.cargar_preparados()
        else:
            StyledPopup.mostrar_popup('Error', mensaje, tipo='error')
