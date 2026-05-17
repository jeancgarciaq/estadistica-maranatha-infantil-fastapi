from sqlalchemy.orm import Session
from controllers.usuarios_controller import UsuariosController
from web.handlers.base_handler import BaseWebHandler
from models.security import ROLE_ROOT
from fastapi import status, Response

class UsuariosWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.controller = UsuariosController(db)

    def _check_root(self, request):
        return request.state.user.rol.nombre == ROLE_ROOT

    async def get_index(self, request):
        if not self._check_root(request):
            return self.redirect("/dashboard", "Acceso restringido al superusuario", "error")
        
        roles = self.controller.listar_roles()
        return self.render(request, "usuarios/index.html", {"roles": roles})

    async def get_list(self, request):
        if not self._check_root(request):
            return Response("Acceso denegado", status_code=status.HTTP_403_FORBIDDEN)
        
        usuarios = self.controller.listar_usuarios()
        return self.render(request, "usuarios/list.html", {"usuarios": usuarios})

    async def post_crear(self, request, datos):
        if not self._check_root(request):
            return self.redirect("/dashboard")
        exito, mensaje = self.controller.registrar_usuario(datos, user_context={"user": request.state.user})
        return self.redirect("/usuarios", mensaje, "success" if exito else "error")

    async def post_actualizar(self, request, user_id, password, rol_nombre, activo):
        if not self._check_root(request):
            return self.redirect("/dashboard")
        
        is_active = True if activo == "on" else False
        exito, mensaje = self.controller.actualizar_usuario(
            user_id=user_id, password=password, rol_nombre=rol_nombre, activo=is_active, 
            user_context={"user": request.state.user}
        )
        return self.redirect("/usuarios", mensaje, "success" if exito else "error")