from sqlalchemy.orm import Session
from controllers.areas_controller import AreasController
from controllers.pastores_controller import PastoresController
from controllers.lideres_controller import LideresController
from controllers.coordinadores_controller import CoordinadoresController
from controllers.capitanes_controller import CapitanesController
from controllers.docentes_controller import DocentesController
from controllers.auxiliares_controller import AuxiliaresController
from controllers.colaboradores_controller import ColaboradoresController
from web.handlers.base_handler import BaseWebHandler
from models.security import ROLE_ROOT

class JerarquiaWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.areas_ctrl = AreasController(db)
        self.pastores_ctrl = PastoresController(db)
        self.lideres_ctrl = LideresController(db)
        self.coordinadores_ctrl = CoordinadoresController(db)
        self.capitanes_ctrl = CapitanesController(db)
        self.docentes_ctrl = DocentesController(db)
        self.auxiliares_ctrl = AuxiliaresController(db)
        self.colaboradores_ctrl = ColaboradoresController(db)

    def _check_admin(self, request):
        return request.state.user.rol.nombre in [ROLE_ROOT, 'administrador']

    # Lógica para Docentes
    async def get_docentes_index(self, request):
        capitanes = self.capitanes_ctrl.listar_capitanes()
        return self.render(request, "docentes/index.html", {"capitanes": capitanes})

    async def get_docentes_list(self, request):
        docentes = self.docentes_ctrl.listar_docentes()
        return self.render(request, "docentes/list.html", {"docentes": docentes})

    async def post_docente_crear(self, request, datos):
        exito, msg = self.docentes_ctrl.crear_docente(datos, user_context={"user": request.state.user})
        return self.redirect("/docentes", msg, "success" if exito else "error")

    async def post_docente_actualizar(self, request, id, datos):
        exito, msg = self.docentes_ctrl.actualizar_docente(id, datos, user_context={"user": request.state.user})
        return self.redirect("/docentes", msg, "success" if exito else "error")

    async def post_docente_eliminar(self, request, id):
        exito, msg = self.docentes_ctrl.eliminar_docente(id, user_context={"user": request.state.user})
        return self.redirect("/docentes", msg, "success" if exito else "error")

    # Lógica para Auxiliares
    async def get_auxiliares_index(self, request):
        capitanes = self.capitanes_ctrl.listar_capitanes()
        return self.render(request, "auxiliares/index.html", {"capitanes": capitanes})

    async def get_auxiliares_list(self, request):
        auxiliares = self.auxiliares_ctrl.listar_auxiliares()
        return self.render(request, "auxiliares/list.html", {"auxiliares": auxiliares})

    async def post_auxiliar_crear(self, request, datos):
        exito, msg = self.auxiliares_ctrl.crear_auxiliar(datos, user_context={"user": request.state.user})
        return self.redirect("/auxiliares", msg, "success" if exito else "error")

    # Lógica para Colaboradores
    async def get_colaboradores_index(self, request):
        capitanes = self.capitanes_ctrl.listar_capitanes()
        return self.render(request, "colaboradores/index.html", {"capitanes": capitanes})

    async def get_colaboradores_list(self, request):
        colaboradores = self.colaboradores_ctrl.listar_colaboradores()
        return self.render(request, "colaboradores/list.html", {"colaboradores": colaboradores})

    async def post_colaborador_crear(self, request, datos):
        exito, msg = self.colaboradores_ctrl.crear_colaborador(datos, user_context={"user": request.state.user})
        return self.redirect("/colaboradores", msg, "success" if exito else "error")

    async def get_pastores_index(self, request):
        if not self._check_admin(request): return self.redirect("/dashboard", "Acceso denegado", "error")
        return self.render(request, "pastores/index.html")

    async def get_pastores_list(self, request):
        pastores = self.pastores_ctrl.listar_pastores()
        return self.render(request, "pastores/list.html", {"pastores": pastores})

    async def post_pastor_crear(self, request, datos):
        exito, msg = self.pastores_ctrl.crear_pastor(datos, user_context={"user": request.state.user})
        return self.redirect("/pastores", msg, "success" if exito else "error")

    # Lógica para Líderes
    async def get_lideres_index(self, request):
        if not self._check_admin(request): return self.redirect("/dashboard", "Acceso denegado", "error")
        pastores = self.pastores_ctrl.listar_pastores()
        return self.render(request, "lideres/index.html", {"pastores": pastores})

    async def get_lideres_list(self, request):
        lideres = self.lideres_ctrl.listar_lideres()
        return self.render(request, "lideres/list.html", {"lideres": lideres})

    # Lógica para Coordinadores
    async def get_coordinadores_index(self, request):
        lideres = self.lideres_ctrl.listar_lideres()
        areas = self.areas_ctrl.listar_areas()
        return self.render(request, "coordinadores/index.html", {"lideres": lideres, "areas": areas})

    async def get_coordinadores_list(self, request):
        coordinadores = self.coordinadores_ctrl.listar_coordinadores()
        return self.render(request, "coordinadores/list.html", {"coordinadores": coordinadores})

    # Lógica para Capitanes
    async def get_capitanes_index(self, request):
        coordinadores = self.coordinadores_ctrl.listar_coordinadores()
        return self.render(request, "capitanes/index.html", {"coordinadores": coordinadores})

    async def get_capitanes_list(self, request):
        try:
            capitanes = self.capitanes_ctrl.listar_capitanes()
            return self.render(request, "capitanes/list.html", {"capitanes": capitanes})
        except Exception as e:
            return self.redirect("/capitanes", f"Error al cargar la lista: {str(e)}", "error")