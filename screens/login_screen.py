from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from components.styled_popup import StyledPopup


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('views/login.kv')
        super().__init__(**kwargs)

    def iniciar_sesion(self):
        username = self.ids.login_username.text.strip()
        password = self.ids.login_password.text.strip()

        app = App.get_running_app()
        if not app:
            StyledPopup.mostrar_popup('Error', 'No se encontró la aplicación activa.', tipo='error')
            return

        exito, usuario, mensaje = app.usuarios_controller.autenticar(username, password)
        if not exito:
            StyledPopup.mostrar_popup('Acceso denegado', mensaje, tipo='error')
            return

        app.set_current_user(usuario)
        self.ids.login_password.text = ''
        app.root.current = 'menu'

    def limpiar(self):
        self.ids.login_username.text = ''
        self.ids.login_password.text = ''
