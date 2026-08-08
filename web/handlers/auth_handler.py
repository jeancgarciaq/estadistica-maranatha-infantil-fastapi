import random
from sqlalchemy.orm import Session
from controllers.usuarios_controller import UsuariosController
from web.handlers.base_handler import BaseWebHandler

class AuthWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.controller = UsuariosController(db)
        # Definimos el prefijo de la subruta
        self.prefix = ""

    async def get_login(self, request):
        return self.render(request, "login.html")

    async def post_login(self, request, username, password):
        exito, usuario, mensaje = self.controller.autenticar(username, password)
        if exito:
            # ✅ REPARADO: Redirige a /semi/dashboard
            response = self.redirect(f"{self.prefix}/dashboard", request=request)
            # Establecer cookie de sesión
            response.set_cookie(key="session_user", value=usuario.username, httponly=True)
            return response
        return self.render(request, "login.html", {"error": mensaje})

    async def get_logout(self, request):
        # ✅ REPARADO: Redirige a /semi (o /semi/login)
        response = self.redirect(f"{self.prefix}/login", request=request)
        response.delete_cookie("session_user")
        return response

    async def get_register(self, request):
        roles = self.controller.listar_roles()
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        return self.render(request, "register.html", {
            "roles": roles,
            "math_challenge": f"¿Cuánto es {num1} + {num2}?",
            "math_result": num1 + num2
        })

    async def post_register(self, request, datos, math_answer, math_expected):
        if not all([datos.get("username"), datos.get("password"), datos.get("rol_nombre"), math_answer is not None]):
            return self._render_register_error(request, "Todos los campos son obligatorios.")

        if math_answer != math_expected:
            return self._render_register_error(request, "Respuesta matemática incorrecta.")

        exito, mensaje = self.controller.registrar_usuario(datos)
        if exito:
            # ✅ REPARADO: Redirige a /semi/login
            return self.redirect(f"{self.prefix}/login", "Registro exitoso. Ya puede iniciar sesión.", "success", request=request)
        
        return self._render_register_error(request, mensaje)

    def _render_register_error(self, request, error_msg):
        roles = self.controller.listar_roles()
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        return self.render(request, "register.html", {
            "error": error_msg,
            "roles": roles,
            "math_challenge": f"¿Cuánto es {num1} + {num2}?",
            "math_result": num1 + num2
        })

    async def get_forgot_password(self, request):
        return self.render(request, "forgot_password.html")

    async def post_forgot_password(self, request, email):
        exito, mensaje = self.controller.solicitar_restablecimiento_contrasena(email, request=request)
        if exito:
            return self.render(request, "forgot_password.html", {
                "message": mensaje,
                "email_sent": True
            })
        return self.render(request, "forgot_password.html", {"error": mensaje})

    async def get_reset_password(self, request, token):
        usuario = self.controller.validar_token_restablecimiento(token)
        if not usuario:
            return self.render(request, "reset_password.html", {
                "error": "El enlace de restablecimiento es inválido o ha expirado."
            })
        return self.render(request, "reset_password.html", {
            "token": token,
            "username": usuario.username
        })

    async def post_reset_password(self, request, token, password, confirm_password):
        if password != confirm_password:
            return self.render(request, "reset_password.html", {
                "token": token,
                "error": "Las contraseñas no coinciden."
            })
        exito, mensaje = self.controller.restablecer_contrasena(token, password)
        if exito:
            # ✅ REPARADO: Redirige a /semi/login
            return self.redirect(f"{self.prefix}/login", "Contraseña restablecida exitosamente.", "success", request=request)
        return self.render(request, "reset_password.html", {"token": token, "error": mensaje})