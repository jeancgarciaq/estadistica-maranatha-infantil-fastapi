import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from components.styled_popup import StyledPopup

class AyudaScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('views/ayuda.kv')
        super().__init__(**kwargs)

    def ir_a(self, screen_name):
        app = App.get_running_app()
        if not app:
            return

        if not app.can_access_screen(screen_name):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para abrir esa sección.', tipo='error')
            return

        self.manager.current = screen_name

    def ir_salones(self):
        app = App.get_running_app()
        if not app:
            return

        self.ir_a('salones' if app.has_permission('salones.manage') else 'lista_salones')

    def ir_aulas(self):
        app = App.get_running_app()
        if not app:
            return

        self.ir_a('aulas' if app.has_permission('aulas.manage') else 'lista_aulas')

    def mostrar_tutoriales(self):
        StyledPopup.mostrar_popup(
            'Tutoriales en camino',
            'Más adelante se agregarán tutoriales en YouTube para cada módulo de la aplicación.\n\n'
            'Por ahora esta ayuda sirve como guía rápida dentro del sistema.',
            tipo='info'
        )