import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty

from components.styled_popup import StyledPopup

class MenuScreen(Screen):
    can_areas = BooleanProperty(False)
    can_salones = BooleanProperty(False)
    can_salones_manage = BooleanProperty(False)
    can_aulas = BooleanProperty(False)
    can_lista_aulas = BooleanProperty(False)
    can_estadistica = BooleanProperty(False)
    can_donaciones = BooleanProperty(False)
    can_preparados = BooleanProperty(False)
    can_distribuciones = BooleanProperty(False)
    can_logistica = BooleanProperty(False)
    can_otras_areas = BooleanProperty(False)
    can_ensenanza = BooleanProperty(False)
    can_recepcion = BooleanProperty(False)
    can_reporte = BooleanProperty(False)
    can_ayuda = BooleanProperty(False)
    can_usuarios = BooleanProperty(False)
    saludo = StringProperty('')

    def __init__(self, **kwargs):
        Builder.load_file('views/menu.kv')
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app or not app.current_user:
            if app and app.root:
                app.root.current = 'login'
            return

        self.saludo = f"Usuario: {app.current_user.username}  |  Rol: {app.current_user.rol.nombre}"

        self.can_areas = app.has_permission('areas.view')
        self.can_salones = app.has_permission('salones.view')
        self.can_salones_manage = app.has_permission('salones.manage')
        self.can_aulas = app.has_permission('aulas.manage')
        self.can_lista_aulas = app.has_permission('aulas.view')
        self.can_estadistica = app.has_permission('estadistica.view')
        self.can_donaciones = app.has_permission('donaciones.view')
        self.can_preparados = app.has_permission('preparados.view')
        self.can_distribuciones = app.has_permission('distribuciones.view')
        self.can_logistica = app.has_permission('logistica.view')
        self.can_otras_areas = app.has_permission('otras_areas.view')
        self.can_ensenanza = app.has_permission('ensenanza.view')
        self.can_recepcion = app.has_permission('recepcion.view')
        self.can_reporte = app.has_permission('reporte.view')
        self.can_ayuda = app.has_permission('ayuda.view')
        self.can_usuarios = app.has_permission('users.manage')

    def ir_a(self, screen_name):
        app = App.get_running_app()
        if not app:
            return
        if not app.can_access_screen(screen_name):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para esta pantalla.', tipo='error')
            return
        self.manager.current = screen_name

    def cerrar_sesion(self):
        app = App.get_running_app()
        if app:
            app.logout()

    def ir_salones(self):
        if self.can_salones_manage:
            self.ir_a('salones')
            return
        self.ir_a('lista_salones')
