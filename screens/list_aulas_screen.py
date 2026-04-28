from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty
from datetime import datetime
import logging

from components.styled_popup import StyledPopup
from components.styled_datepicker import StyledDatePicker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulaCard(BoxLayout):
    aula_id = NumericProperty(0)
    titulo = StringProperty('')
    info = StringProperty('')
    editar_callback = ObjectProperty(allownone=True)
    eliminar_callback = ObjectProperty(allownone=True)
    can_manage = BooleanProperty(True)


class ListAulasScreen(Screen):
    """ Pantalla que muestra una lista de aulas. """
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_aulas.kv')
        except Exception as e:
            logger.error(f"Error al cargar list_aulas.kv: {e}")
        super().__init__(**kwargs)
        logger.info("Initializando ListAulasScreen")
        # Crear el controlador como atributo
        self.controlador = controlador
        self.fecha_filtro = ""
        self.can_manage = False

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app or not app.can_access_screen('lista_aulas'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para ver la lista de aulas.', tipo='error')
            if app and app.root:
                app.root.current = 'menu'
            return
        self.can_manage = app.has_permission('aulas.manage')

    def abrir_datepicker(self, target_id):
        """Abre el selector de fecha para filtrar la lista."""
        def set_date(date_str):
            self.ids[target_id].text = date_str

        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def editar_aula(self, aula_id):
        if not self.can_manage:
            StyledPopup.mostrar_popup('Acceso denegado', 'Solo puede visualizar aulas.', tipo='error')
            return
        app = App.get_running_app()
        if not app or not app.root:
            StyledPopup.mostrar_popup('Error', 'No se pudo abrir la pantalla de aulas.', tipo='error')
            return

        aulas_screen = app.root.get_screen('aulas')
        aulas_screen.editar_aula(aula_id)
        app.root.current = 'aulas'

    def eliminar_aula(self, aula_id):
        if not self.can_manage:
            StyledPopup.mostrar_popup('Acceso denegado', 'Solo puede visualizar aulas.', tipo='error')
            return
        exito, mensaje = self.controlador.eliminar_aula(int(aula_id))
        if exito:
            StyledPopup.mostrar_popup('Éxito', mensaje, tipo='success')
            self.cargar_aulas()
        else:
            StyledPopup.mostrar_popup('Error', mensaje, tipo='error')

    def obtener_fecha_filtro(self):
        fecha = self.ids.fecha_filtro.text.strip()
        if not fecha:
            StyledPopup.mostrar_popup('Error', 'Debe seleccionar una fecha para listar las aulas.', tipo='error')
            return None

        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup('Error', 'La fecha debe tener el formato YYYY-MM-DD.', tipo='error')
            return None

        return fecha

    def listar_aulas_por_fecha(self):
        fecha = self.obtener_fecha_filtro()
        if not fecha:
            return

        try:
            aulas = self.controlador.listar_aulas_por_fecha(fecha)
            if aulas is None:
                logger.warning("El método listar_aulas_por_fecha devolvió None.")
                aulas = []
            self.actualizar_lista_aulas(aulas)
        except Exception as e:
            logger.error(f"Error consultando aulas por fecha: {e}")
            self.actualizar_lista_aulas([])

    def limpiar_filtro_fecha(self):
        """Limpia la fecha seleccionada y reinicia la lista."""
        if 'fecha_filtro' in self.ids:
            self.ids.fecha_filtro.text = ''
        self.actualizar_lista_aulas([])
        

    def actualizar_lista_aulas(self, aulas):
        """Actualiza la lista de aulas en la vista."""
        logger.debug(f"Datos recibidos para actualizar lista de aulas: {aulas}")
        if not isinstance(aulas, list):
            logger.error("El parámetro 'aulas' no es una lista. Verifique el controlador.")
            aulas = []
        lista_aulas = self.ids.lista_aulas
        lista_aulas.clear_widgets()
        if not aulas or len(aulas) == 0:
            lista_aulas.add_widget(Label(text="No hay aulas registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for aula in aulas: 
                try:
                    nombre_salon = getattr(getattr(aula, 'salon', None), 'salon', None)
                except Exception:
                    nombre_salon = None
                if not nombre_salon:
                    nombre_salon = f"ID {getattr(aula, 'id_salon', 'N/D')}"
                fecha = aula.fecha.strftime('%Y-%m-%d') if hasattr(aula.fecha, 'strftime') else str(aula.fecha)
                lista_aulas.add_widget(AulaCard(
                    aula_id=aula.id,
                    titulo=f"Aula {aula.id}",
                    info=(
                        f"Salón: {nombre_salon} | Fecha: {fecha}\n"
                        f"Maestra: {aula.maestra} | Condición: {aula.condicion}\n"
                        f"Auxiliar: {aula.auxiliar} | Capitán: {aula.capitan} | Colaborador: {aula.colaborador}\n"
                        f"Niños: {aula.ninos} | Niñas: {aula.ninas} | Subcapitán: {aula.subcapitan}"
                    ),
                    editar_callback=self.editar_aula,
                    eliminar_callback=self.eliminar_aula,
                    can_manage=self.can_manage,
                ))
            
    def cargar_aulas(self):
        """Consultando y llenando la lista aulas."""
        if not self.controlador:
            logger.error("El controlador no está inicializado. No se pueden listar las donaciones.")
            return
        self.listar_aulas_por_fecha()
    
    def on_enter(self, *args):
        """Llamando cuando la pantalla está completa."""
        self.actualizar_lista_aulas([])

    def volver(self, instance):
        """Regresa a la pantalla de aulas"""
        self.manager.current = 'aulas'


