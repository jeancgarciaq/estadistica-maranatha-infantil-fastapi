from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.factory import Factory
from components.styled_datepicker import StyledDatePicker
from datetime import datetime
import logging

from components.styled_popup import StyledPopup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
try:
    Builder.load_file('views/list_preparados.kv')
except Exception as e:
    logger.error(f"Error cargando list_preparados.kv: {e}")

class ListPreparadosScreen(Screen):
    fecha_filtro = StringProperty("")

    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador

    def abrir_datepicker_filtro(self):
        """Abre el selector de fecha para filtrar registros."""
        def set_date(date_str):
            self.fecha_filtro = date_str
            self.cargar_preparados()

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

    def on_enter(self):
        if not self.fecha_filtro:
            self.fecha_filtro = datetime.now().strftime('%Y-%m-%d')
        self.actualizar_lista([]) # Iniciar con la lista vacía hasta filtrar

    def cargar_preparados(self):
        fecha = self._obtener_fecha_filtro()
        if not fecha:
            return

        try:
            preparados = self.controlador.listar_preparados(fecha=fecha)
            self.actualizar_lista(preparados)
        except Exception as e:
            logger.error(f"Error al cargar preparados: {e}")
            self.actualizar_lista([])

    def actualizar_lista(self, preparados):
        contenedor = self.ids.lista_preparados
        contenedor.clear_widgets()

        if not preparados:
            contenedor.add_widget(Label(text='No hay alimentos preparados registrados.', size_hint_y=None, height=40))
            return

        for preparado in preparados:
            # Usamos la Factory para instanciar la tarjeta definida en el .kv
            tarjeta = Factory.PreparadoCard()
            tarjeta.preparado_id = str(preparado.id)
            tarjeta.nombre = preparado.descripcion
            tarjeta.cantidad = f"{preparado.cantidad} {preparado.unidad}"
            tarjeta.fecha = str(preparado.fecha)
            
            contenedor.add_widget(tarjeta)

    def editar_registro(self, preparado_id):
        """Lógica para editar el registro (redirigir a pantalla de combinación)."""
        # Aquí puedes implementar la lógica para cargar los datos en la pantalla de edición
        logger.info(f"Editando preparado ID: {preparado_id}")

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
