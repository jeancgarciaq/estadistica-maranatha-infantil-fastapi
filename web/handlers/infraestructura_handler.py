from sqlalchemy.orm import Session
from controllers.areas_controller import AreasController
from controllers.salones_controller import SalonesController
from controllers.aulas_controller import AulasController
from controllers.recepcion_controller import RecepcionController
from controllers.ensenanza_controller import EnsenanzaController
from controllers.logistica_controller import LogisticaController
from controllers.otras_areas_controller import OtrasAreasController
from controllers.servidor_controller import ServidorController
from web.handlers.base_handler import BaseWebHandler

class InfraestructuraWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.areas_ctrl = AreasController(db)
        self.salones_ctrl = SalonesController(db)
        self.aulas_ctrl = AulasController(db)
        self.recepcion_ctrl = RecepcionController(db)
        self.ensenanza_ctrl = EnsenanzaController(db)
        self.logistica_ctrl = LogisticaController(db)
        self.otrasareas_ctrl = OtrasAreasController(db)
        self.serv_ctrl = ServidorController(db)

    # Áreas
    async def get_areas_index(self, request):
        return self.render(request, "areas/index.html")

    async def get_areas_list(self, request):
        areas = self.areas_ctrl.listar_areas()
        return self.render(request, "areas/list.html", {"areas": areas})

    async def post_area_crear(self, request, nombre):
        exito, msg = self.areas_ctrl.crear_area(nombre, user_context={"user": request.state.user})
        return self.redirect("/areas", msg, "success" if exito else "error")

    async def post_area_actualizar(self, request, id, nombre):
        exito, msg = self.areas_ctrl.actualizar_area(id, nombre, user_context={"user": request.state.user})
        return self.redirect("/areas", msg, "success" if exito else "error")

    async def post_area_eliminar(self, request, id):
        exito, msg = self.areas_ctrl.eliminar_area(id, user_context={"user": request.state.user})
        return self.redirect("/areas", msg, "success" if exito else "error")

    # Salones
    async def get_salones_index(self, request):
        return self.render(request, "salones/index.html")

    async def get_salones_list(self, request):
        salones = self.salones_ctrl.listar_salones()
        return self.render(request, "salones/list.html", {"salones": salones})

    async def post_salon_crear(self, request, nombre, edad):
        exito, msg = self.salones_ctrl.crear_salon(nombre, edad, user_context={"user": request.state.user})
        return self.redirect("/salones", msg, "success" if exito else "error")

    async def post_salon_actualizar(self, request, id, nombre, edad):
        exito, msg = self.salones_ctrl.actualizar_salon(id, nombre, edad, user_context={"user": request.state.user})
        return self.redirect("/salones", msg, "success" if exito else "error")

    async def post_salon_eliminar(self, request, id):
        exito, msg = self.salones_ctrl.eliminar_salon(id, user_context={"user": request.state.user})
        return self.redirect("/salones", msg, "success" if exito else "error")

    # Recepciones
    async def get_recepciones_index(self, request):
        return self.render(request, "recepciones/index.html")

    async def get_recepciones_list(self, request):
        recepciones = self.recepcion_ctrl.listar_recepciones()
        return self.render(request, "recepciones/list.html", {"recepciones": recepciones})

    async def post_recepcion_crear(self, request, nombre, fecha):
        exito, msg = self.recepcion_ctrl.crear_recepcion(nombre, fecha, user_context={"user": request.state.user})
        return self.redirect("/recepciones", msg, "success" if exito else "error")

    async def post_recepcion_actualizar(self, request, id, nombre, fecha):
        exito, msg = self.recepcion_ctrl.actualizar_recepcion(id, nombre, fecha, user_context={"user": request.state.user})
        return self.redirect("/recepciones", msg, "success" if exito else "error")

    async def post_recepcion_eliminar(self, request, id):
        exito, msg = self.recepcion_ctrl.eliminar_recepcion(id, user_context={"user": request.state.user})
        return self.redirect("/recepciones", msg, "success" if exito else "error")

    # Aulas
    async def get_aulas_index(self, request):
        salones = self.salones_ctrl.listar_salones()
        servidores = self.serv_ctrl.listar_servidores()
        return self.render(request, "aulas/index.html", {"salones": salones, "servidores": servidores})

    async def get_aulas_list(self, request, fecha=None):
        aulas = self.aulas_ctrl.listar_aulas_por_fecha(fecha=fecha)
        return self.render(request, "aulas/list.html", {"aulas": aulas, "fecha_filtro": fecha})

    async def post_aula_crear(self, request, datos):
        exito, msg = self.aulas_ctrl.crear_aula_con_asistencia(datos, user_context={"user": request.state.user})
        return self.redirect("/aulas", msg, "success" if exito else "error")

    async def post_aula_actualizar(self, request, id, datos):
        exito, msg = self.aulas_ctrl.actualizar_aula(id, datos, user_context={"user": request.state.user})
        return self.redirect("/aulas", msg, "success" if exito else "error")

    async def post_aula_eliminar(self, request, id):
        exito, msg = self.aulas_ctrl.eliminar_aula(id, user_context={"user": request.state.user})
        return self.redirect("/aulas", msg, "success" if exito else "error")

    # Enseñanza
    async def get_ensenanza_index(self, request):
        return self.render(request, "ensenanza/index.html")

    async def get_ensenanza_list(self, request):
        registros = self.ensenanza_ctrl.listar_ensenanzas()
        return self.render(request, "ensenanza/list.html", {"registros": registros})

    async def post_ensenanza_crear(self, request, capitan, subcapitan, fecha):
        exito, msg = self.ensenanza_ctrl.crear_ensenanza(capitan, fecha, subcapitan, user_context={"user": request.state.user})
        return self.redirect("/ensenanza", msg, "success" if exito else "error")

    async def post_ensenanza_actualizar(self, request, id, capitan, subcapitan, fecha):
        exito, msg = self.ensenanza_ctrl.actualizar_ensenanza(id, capitan, subcapitan, fecha, user_context={"user": request.state.user})
        return self.redirect("/ensenanza", msg, "success" if exito else "error")

    async def post_ensenanza_eliminar(self, request, id):
        exito, msg = self.ensenanza_ctrl.eliminar_ensenanza(id, user_context={"user": request.state.user})
        return self.redirect("/ensenanza", msg, "success" if exito else "error")

    # Logística
    async def get_logistica_index(self, request):
        servidores = self.serv_ctrl.listar_servidores()
        return self.render(request, "logistica/index.html", {"servidores": servidores})

    async def get_logistica_list(self, request, fecha=None):
        logisticas = self.logistica_ctrl.listar_logisticas(fecha=fecha)
        return self.render(request, "logistica/list.html", {"logisticas": logisticas, "fecha_filtro": fecha})

    async def post_logistica_crear(self, request, datos):
        exito, msg = self.logistica_ctrl.crear_logistica_con_asistencia(datos, user_context={"user": request.state.user})
        return self.redirect("/logistica", msg, "success" if exito else "error")

    async def post_logistica_actualizar(self, request, id, datos):
        exito, msg = self.logistica_ctrl.actualizar_logistica(id, datos, user_context={"user": request.state.user})
        return self.redirect("/logistica", msg, "success" if exito else "error")

    async def post_logistica_eliminar(self, request, id):
        exito, msg = self.logistica_ctrl.eliminar_logistica(id, user_context={"user": request.state.user})
        return self.redirect("/logistica", msg, "success" if exito else "error")

    # Otras Áreas
    async def get_otrasareas_index(self, request):
        return self.render(request, "otrasareas/index.html")

    async def get_otrasareas_list(self, request, fecha=None):
        registros = self.otrasareas_ctrl.listar_otrasareas(fecha=fecha)
        return self.render(request, "otrasareas/list.html", {"registros": registros, "fecha_filtro": fecha})

    async def post_otrasareas_crear(self, request, datos):
        exito, msg = self.otrasareas_ctrl.crear_otrasareas(datos, user_context={"user": request.state.user})
        return self.redirect("/otras_areas", msg, "success" if exito else "error")

    async def post_otrasareas_actualizar(self, request, id, datos):
        exito, msg = self.otrasareas_ctrl.actualizar_otrasareas(id, datos, user_context={"user": request.state.user})
        return self.redirect("/otras_areas", msg, "success" if exito else "error")

    async def post_otrasareas_eliminar(self, request, id):
        exito, msg = self.otrasareas_ctrl.eliminar_otrasareas(id, user_context={"user": request.state.user})
        return self.redirect("/otras_areas", msg, "success" if exito else "error")