import json
from sqlalchemy.orm import Session
from controllers.donaciones_controller import DonacionesController
from controllers.distribucion_controller import DistribucionesController
from web.handlers.base_handler import BaseWebHandler
from utils.config_loader import obtener_medidas
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.salones import Salon
from models.areas import Area
from models.recepcion import Recepcion

class AlimentosWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.db = db
        self.don_ctrl = DonacionesController(db)
        self.dist_ctrl = DistribucionesController(db)

    # --- DONACIONES (Materias Primas) ---
    async def get_donaciones_index(self, request):
        return self.render(request, "donaciones/index.html", {"medidas": obtener_medidas()})

    async def get_donaciones_list(self, request, fecha=None):
        donaciones = self.don_ctrl.listar_donaciones(fecha=fecha)
        return self.render(request, "donaciones/list.html", {"donaciones": donaciones, "fecha_filtro": fecha})

    async def post_donacion_crear(self, request, datos):
        exito, msg = self.don_ctrl.crear_donacion(datos, user_context={"user": request.state.user})
        return self.redirect("/donaciones", msg, "success" if exito else "error")

    # --- PREPARADOS (Producción) ---
    async def get_preparados_index(self, request):
        return self.render(request, "preparados/index.html", {"medidas": obtener_medidas()})

    async def get_preparados_list(self, request, fecha=None):
        preparados = self.don_ctrl.listar_preparados(fecha=fecha)
        return self.render(request, "preparados/list.html", {"preparados": preparados, "fecha_filtro": fecha})

    async def post_preparado_crear(self, request, datos_res, componentes_json):
        try:
            lista_comp = json.loads(componentes_json)
            exito, msg = self.don_ctrl.combinar_donaciones(datos_res, lista_comp, user_context={"user": request.state.user})
            return self.redirect("/preparados", msg, "success" if exito else "error")
        except Exception as e:
            return self.redirect("/preparados", f"Error de formato: {str(e)}", "error")

    # --- DISTRIBUCIONES (Logística) ---
    async def get_distribuciones_index(self, request):
        context = {
            "donaciones": self.db.query(Donacion).filter(Donacion.cantidad > 0, Donacion.is_deleted == False).all(),
            "preparados": self.db.query(AlimentoPreparado).filter(AlimentoPreparado.cantidad > 0, AlimentoPreparado.is_deleted == False).all(),
            "salones": self.db.query(Salon).filter(Salon.is_deleted == False).all(),
            "areas": self.db.query(Area).filter(Area.is_deleted == False).all(),
            "recepciones": self.db.query(Recepcion).filter(Recepcion.is_deleted == False).all(),
            "medidas": obtener_medidas()
        }
        return self.render(request, "distribuciones/index.html", context)

    async def get_distribuciones_list(self, request, fecha=None):
        distribuciones = self.dist_ctrl.listar_distribuciones(fecha=fecha)
        return self.render(request, "distribuciones/list.html", {"distribuciones": distribuciones, "fecha_filtro": fecha})

    async def post_distribucion_crear(self, request, datos):
        exito, msg = self.dist_ctrl.crear_distribucion(datos, user_context={"user": request.state.user})
        return self.redirect("/distribuciones", msg, "success" if exito else "error")

    async def post_distribucion_eliminar(self, request, id):
        exito, msg = self.dist_ctrl.eliminar_distribucion(id, user_context={"user": request.state.user})
        return self.redirect("/distribuciones", msg, "success" if exito else "error")

    # --- APIS ---
    async def api_materias_primas(self):
        materias = self.db.query(Donacion).filter(Donacion.cantidad > 0, Donacion.is_deleted == False).all()
        return [{"id": m.id, "descripcion": m.descripcion, "cantidad": m.cantidad, "unidad": m.unidad} for m in materias]

    async def api_medidas(self):
        return {"unidades": obtener_medidas()}