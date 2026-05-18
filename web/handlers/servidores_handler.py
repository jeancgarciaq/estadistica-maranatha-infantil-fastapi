from sqlalchemy.orm import Session
from controllers.servidor_controller import ServidorController
from controllers.areas_controller import AreasController
from controllers.capitanes_controller import CapitanesController
from controllers.usuarios_controller import UsuariosController
from web.handlers.base_handler import BaseWebHandler
from fastapi import Response, HTTPException

class ServidoresWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.controller = ServidorController(db)
        self.areas_ctrl = AreasController(db)
        self.capitanes_ctrl = CapitanesController(db)

    async def get_index(self, request):
        if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.view"):
            return self.redirect("/dashboard", "Acceso restringido", "error")
        
        areas = self.areas_ctrl.listar_areas()
        capitanes = self.capitanes_ctrl.listar_capitanes()
        return self.render(request, "servidores/index.html", {"areas": areas, "capitanes": capitanes})

    async def get_list(self, request, filtros: dict):
        if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.view"):
            return Response("Acceso denegado", status_code=403)
        
        servidores = self.controller.listar_servidores()
        return self.render(request, "servidores/list.html", {
            "servidores": servidores,
            "areas": self.areas_ctrl.listar_areas(),
            "capitanes": self.capitanes_ctrl.listar_capitanes()
        })

    async def post_crear(self, request, datos: dict):
        if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
            return self.redirect("/servidores", "No tiene permisos para crear", "error")
        
        exito, mensaje = self.controller.crear_servidor(datos, user_context={"user": request.state.user})
        return self.redirect("/servidores", mensaje, "success" if exito else "error")

    async def post_actualizar(self, request, id: int, datos: dict):
        if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
            return self.redirect("/servidores", "No tiene permisos para editar", "error")

        exito, mensaje = self.controller.actualizar_servidor(id, datos, user_context={"user": request.state.user})
        return self.redirect("/servidores", mensaje, "success" if exito else "error")

    async def post_eliminar(self, request, id: int):
        if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
            return self.redirect("/servidores", "No tiene permisos para eliminar", "error")

        exito, mensaje = self.controller.eliminar_servidor(id, user_context={"user": request.state.user})
        return self.redirect("/servidores", mensaje, "success" if exito else "error")

    async def exportar(self, request, formato: str, filtros: dict):
        servidores = self.controller.listar_servidores()
        if formato == "pdf":
            content = self.controller.generar_reporte_pdf(servidores)
            return Response(content=content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=servidores.pdf"})
        elif formato == "excel":
            content = self.controller.generar_reporte_excel(servidores)
            return Response(content=content, media_type="application/vnd.ms-excel", headers={"Content-Disposition": "attachment; filename=servidores.xlsx"})
        return self.redirect("/servidores", "Formato no soportado", "error")
