from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from components.styled_popup import StyledPopup
from components.styled_datepicker import StyledDatePicker
from kivy.factory import Factory
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
Builder.load_file('views/list_otras_areas.kv')

class ListOtrasAreasScreen(Screen):
    
    fecha_filtro = StringProperty("")

    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador

    def abrir_datepicker_filtro(self):
        """Abre el selector de fecha para filtrar registros."""
        def set_date(date_str):
            self.fecha_filtro = date_str
            self.cargar_datos()

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
            StyledPopup.mostrar_popup("Error", "Formato de fecha inválido. Use YYYY-MM-DD.", tipo="error")
            return None

    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        if not self.fecha_filtro:
            self.fecha_filtro = datetime.now().strftime('%Y-%m-%d')
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los registros desde el controlador."""
        fecha = self._obtener_fecha_filtro()
        if not fecha:
            return

        try:
            registros = self.controlador.listar_otrasareas(fecha=fecha)
            self.actualizar_lista(registros)
        except Exception as e:
            logger.error(f"Error al cargar datos de otras áreas: {e}")
            StyledPopup.mostrar_popup("Error", f"No se pudieron cargar los datos: {e}", tipo="error")

    def actualizar_lista(self, registros):
        """Puebla el contenedor con los registros."""
        if 'container' not in self.ids:
            logger.error("El widget 'container' no está definido en el archivo .kv.")
            return
            
        container = self.ids.container
        container.clear_widgets()

        if not registros:
            container.add_widget(Label(text="No hay registros disponibles", size_hint_y=None, height=40))
            return

        for reg in registros:
            fecha_str = reg.fecha.strftime('%Y-%m-%d') if hasattr(reg.fecha, 'strftime') else str(reg.fecha or '')
            area_nombre = "Registro de Otras Áreas"

            card = Factory.AreaCard()
            card.area_id = str(reg.id)
            card.area_nombre = area_nombre
            card.fecha = fecha_str
            card.alabanza = str(reg.alabanza)
            card.protocolo = str(reg.protocolo)
            card.semillitas = str(reg.semillitas)
            card.sonido = str(reg.sonido)
            card.teatro = str(reg.teatro)
            card.tv = str(reg.tv)
            card.ujier = str(reg.ujier)
            card.seguridad = str(reg.seguridad)

            container.add_widget(card)

    def editar_registro(self, registro_id):
        """Regresa a la pantalla principal y carga el registro para editar."""
        registro_id = int(registro_id)
        self.manager.current = 'otrasareas'
        main_screen = self.manager.get_screen('otrasareas')
        main_screen.editar_otrasareas(registro_id)

    def confirmar_eliminacion(self, registro_id):
        """Muestra el popup de confirmación antes de borrar."""
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            "Esta acción no se puede deshacer. ¿Está seguro de que desea eliminar este registro?",
            on_confirm=lambda: self.eliminar_registro(registro_id)
        )

    def eliminar_registro(self, registro_id):
        """Ejecuta la eliminación final del registro."""
        registro_id = int(registro_id)
        exito, mensaje = self.controlador.eliminar_otrasareas(registro_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_datos() # Refrescar lista
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")
