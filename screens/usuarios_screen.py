from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen

from components.styled_popup import StyledPopup
from models.security import ROLE_ROOT


class UsuariosScreen(Screen):
    roles = ListProperty([])
    selected_user_id = None
    selected_username = ''
    selected_role = ''
    selected_active = True
    puede_editar_root = BooleanProperty(False)
    selected_is_root = BooleanProperty(False)

    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/usuarios.kv')
        super().__init__(**kwargs)
        self.controlador = controlador

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app or not app.has_permission('users.manage'):
            StyledPopup.mostrar_popup('Acceso denegado', 'Solo el usuario root puede gestionar usuarios.', tipo='error')
            if app and app.root:
                app.root.current = 'menu'
            return

        self.cargar_roles()
        self.cargar_usuarios()

    def cargar_roles(self):
        roles = self.controlador.listar_roles()
        self.roles = [r.nombre for r in roles]
        if self.roles and self.ids.user_role.text not in self.roles:
            self.ids.user_role.text = self.roles[0]

    def cargar_usuarios(self):
        usuarios = self.controlador.listar_usuarios()
        data = []
        for usuario in usuarios:
            data.append({
                'user_id': usuario.id,
                'username': usuario.username,
                'password': usuario.password,
                'role': usuario.rol.nombre if usuario.rol else '',
                'active': 'SI' if usuario.activo else 'NO',
            })
        self.ids.users_rv.data = data

    def seleccionar_usuario(self, item):
        self.selected_user_id = item.get('user_id')
        self.selected_username = item.get('username', '')
        self.selected_role = item.get('role', '')
        self.selected_active = item.get('active', 'SI') == 'SI'
        self.selected_is_root = self.selected_username == 'root'

        self.ids.user_username.text = self.selected_username
        self.ids.user_password.text = item.get('password', '')
        if self.selected_role in self.roles:
            self.ids.user_role.text = self.selected_role

        self.puede_editar_root = not self.selected_is_root
        self.ids.user_active.active = self.selected_active

    def crear_usuario(self):
        username = self.ids.user_username.text.strip()
        password = self.ids.user_password.text.strip()
        rol = self.ids.user_role.text.strip()

        exito, mensaje = self.controlador.crear_usuario(username, password, rol)
        if exito:
            StyledPopup.mostrar_popup('Exito', mensaje, tipo='success')
            self.limpiar_formulario()
            self.cargar_usuarios()
        else:
            StyledPopup.mostrar_popup('Error', mensaje, tipo='error')

    def actualizar_usuario(self):
        if not self.selected_user_id:
            StyledPopup.mostrar_popup('Error', 'Debe seleccionar un usuario de la lista.', tipo='error')
            return

        username_actual = self.selected_username
        password = self.ids.user_password.text.strip()
        rol = self.ids.user_role.text.strip()
        activo = self.ids.user_active.active

        if username_actual == 'root' and rol != ROLE_ROOT:
            StyledPopup.mostrar_popup('Error', 'El usuario root debe mantener su rol root.', tipo='error')
            return

        if username_actual == 'root':
            activo = True

        exito, mensaje = self.controlador.actualizar_usuario(
            user_id=self.selected_user_id,
            password=password,
            rol_nombre=rol,
            activo=activo,
        )
        if exito:
            StyledPopup.mostrar_popup('Exito', mensaje, tipo='success')
            self.cargar_usuarios()
        else:
            StyledPopup.mostrar_popup('Error', mensaje, tipo='error')

    def limpiar_formulario(self):
        self.selected_user_id = None
        self.selected_username = ''
        self.selected_role = ''
        self.selected_active = True
        self.puede_editar_root = False
        self.selected_is_root = False

        self.ids.user_username.text = ''
        self.ids.user_password.text = ''
        if self.roles:
            self.ids.user_role.text = self.roles[0]
        self.ids.user_active.active = True

    def volver_menu(self):
        self.manager.current = 'menu'
