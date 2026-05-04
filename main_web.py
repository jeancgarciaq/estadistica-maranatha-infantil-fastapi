import os
import logging
import json
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from models.database import get_db, configure_database
from utils.env_loader import load_app_env
from utils.firebase_auth import FirebaseAuthService, FirebaseAuthSession
from utils.config_loader import obtener_medidas

from controllers.areas_controller import AreasController
from controllers.aulas_controller import AulasController
from controllers.salones_controller import SalonesController
from controllers.donaciones_controller import DonacionesController
from controllers.ensenanza_controller import EnsenanzaController
from utils.reporte_estadistico import ReporteEstadisticoService
from controllers.otras_areas_controller import OtrasAreasController
from controllers.recepcion_controller import RecepcionController
from controllers.logistica_controller import LogisticaController
from controllers.distribucion_controller import DistribucionesController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_app_env()

# Inicializar Base de Datos
configure_database()

# Inicializar FastAPI
app = FastAPI(title="Estadística Maranatha Infantil - Web")
security = HTTPBearer()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Servicio de Autenticación Firebase
auth_service = FirebaseAuthService()

# Middleware de Autenticación y Autorización
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Rutas que no requieren autenticación
    # Quitamos "/" de la lista para evitar que coincida con todo vía startswith
    public_paths = ["/login", "/logout", "/static", "/api/config/medidas"]
    
    if request.url.path == "/" or any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Obtener tokens y datos de sesión de las cookies
    id_token = request.cookies.get("id_token")
    local_id = request.cookies.get("local_id")
    email = request.cookies.get("email")

    if not id_token:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        # Reconstruir la sesión y validar el rol en Firebase
        session = auth_service.reconstruct_session(id_token, local_id=local_id, email=email)
        role_assignment = auth_service.fetch_role_assignment(session)
        request.state.user = auth_service.build_runtime_user(session, role_assignment)
    except Exception as e:
        logger.error("Error de autenticación en middleware: %s", e)
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("id_token")
        return response

    return await call_next(request)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        # Intentar iniciar sesión en Firebase
        session_data = auth_service.sign_in(username, password)
        
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        
        # Persistir sesión en cookies seguras
        response.set_cookie(key="id_token", value=session_data.id_token)
        response.set_cookie(key="local_id", value=session_data.local_id, httponly=True)
        response.set_cookie(key="email", value=session_data.email, httponly=True)
        
        return response
    except Exception as e:
        logger.error("Error de login: %s", e)
        return templates.TemplateResponse(request, "login.html", {"error": str(e)})

@app.get("/donaciones", response_class=HTMLResponse)
async def view_donaciones(request: Request):
    medidas = obtener_medidas()
    return templates.TemplateResponse(request, "donaciones/index.html", {
        "user": request.state.user,
        "medidas": medidas
    })

@app.get("/donaciones/lista", response_class=HTMLResponse)
async def list_donaciones(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = DonacionesController(session=db)
    donaciones = controller.listar_donaciones(fecha=fecha)
    return templates.TemplateResponse(request, "donaciones/list.html", {
        "donaciones": donaciones,
        "user": request.state.user,
        "fecha_filtro": fecha
    })

@app.post("/donaciones/crear")
async def create_donacion(
    request: Request,
    descripcion: str = Form(...),
    cantidad: float = Form(...),
    unidad: str = Form(...),
    fecha: str = Form(...),
    equipo: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = DonacionesController(session=db)
    datos = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    exito, mensaje = controller.crear_donacion(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/donaciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/donaciones/actualizar")
async def update_donacion(
    request: Request,
    id: int = Form(...),
    descripcion: str = Form(...),
    cantidad: float = Form(...),
    unidad: str = Form(...),
    fecha: str = Form(...),
    equipo: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = DonacionesController(session=db)
    datos = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    exito, mensaje = controller.actualizar_donacion(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/donaciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/donaciones/eliminar")
async def delete_donacion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = DonacionesController(session=db)
    exito, mensaje = controller.eliminar_donacion(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/donaciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/preparados", response_class=HTMLResponse)
async def view_preparados(request: Request):
    return templates.TemplateResponse(request, "preparados/index.html", {
        "user": request.state.user,
        "medidas": obtener_medidas()
    })

@app.get("/preparados/lista", response_class=HTMLResponse)
async def list_preparados(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = DonacionesController(session=db)
    preparados = controller.listar_preparados(fecha=fecha)
    return templates.TemplateResponse(request, "preparados/list.html", {
        "user": request.state.user,
        "preparados": preparados,
        "fecha_filtro": fecha
    })

@app.post("/preparados/crear")
async def create_preparado(
    request: Request,
    descripcion: str = Form(...),
    cantidad: float = Form(...),
    unidad: str = Form(...),
    fecha: str = Form(...),
    equipo: str = Form(...),
    componentes_json: str = Form(...), # Recibimos la lista de ingredientes como JSON desde el frontend
    db: Session = Depends(get_db)
):
    controller = DonacionesController(session=db)
    datos_res = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    try:
        lista_comp = json.loads(componentes_json)
        exito, mensaje = controller.combinar_donaciones(datos_res, lista_comp, user_context={"user": request.state.user})
        return RedirectResponse(url=f"/preparados?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return RedirectResponse(url=f"/preparados?msg=Error: {str(e)}&type=error", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/distribuciones", response_class=HTMLResponse)
async def view_distribuciones(request: Request, db: Session = Depends(get_db)):
    from models.donaciones import Donacion
    from models.alimento_preparado import AlimentoPreparado
    from models.salones import Salon
    from models.areas import Area
    from models.recepcion import Recepcion
    
    donaciones = db.query(Donacion).filter(Donacion.cantidad > 0, Donacion.is_deleted == False).all()
    preparados = db.query(AlimentoPreparado).filter(AlimentoPreparado.cantidad > 0, AlimentoPreparado.is_deleted == False).all()
    salones = db.query(Salon).filter(Salon.is_deleted == False).all()
    areas = db.query(Area).filter(Area.is_deleted == False).all()
    recepciones = db.query(Recepcion).filter(Recepcion.is_deleted == False).all()

    return templates.TemplateResponse(request, "distribuciones/index.html", {
        "user": request.state.user,
        "donaciones": donaciones,
        "preparados": preparados,
        "salones": salones,
        "areas": areas,
        "recepciones": recepciones,
        "medidas": obtener_medidas()
    })

@app.get("/distribuciones/lista", response_class=HTMLResponse)
async def list_distribuciones(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = DistribucionesController(session=db)
    distribuciones = controller.listar_distribuciones(fecha=fecha)
    return templates.TemplateResponse(request, "distribuciones/list.html", {
        "user": request.state.user,
        "distribuciones": distribuciones,
        "fecha_filtro": fecha
    })

@app.post("/distribuciones/crear")
async def create_distribucion(
    request: Request,
    donacion_id: int = Form(None),
    alimento_preparado_id: int = Form(None),
    salon_id: int = Form(None),
    area_id: int = Form(None),
    recepcion_id: int = Form(None),
    cantidad: float = Form(...),
    unidad: str = Form(...),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = DistribucionesController(session=db)
    datos = {
        "donacion_id": donacion_id, "alimento_preparado_id": alimento_preparado_id,
        "salon_id": salon_id, "area_id": area_id, "recepcion_id": recepcion_id,
        "cantidad": cantidad, "unidad": unidad, "fecha": fecha
    }
    exito, mensaje = controller.crear_distribucion(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/distribuciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/distribuciones/eliminar")
async def delete_distribucion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = DistribucionesController(session=db)
    exito, mensaje = controller.eliminar_distribucion(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/distribuciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/api/materias-primas")
async def get_materias_primas(db: Session = Depends(get_db)):
    """Endpoint para buscar donaciones con stock (Materias Primas)"""
    from models.donaciones import Donacion
    materias = db.query(Donacion).filter(Donacion.cantidad > 0, Donacion.is_deleted == False).all()
    return [{"id": m.id, "descripcion": m.descripcion, "cantidad": m.cantidad, "unidad": m.unidad} for m in materias]

@app.get("/api/config/medidas")
async def get_medidas():
    """Endpoint para que el frontend JS obtenga las unidades de medida para los select/dropdowns."""
    return {"unidades": obtener_medidas()}

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {
        "user": request.state.user
    })

@app.get("/areas", response_class=HTMLResponse)
async def view_areas(request: Request):
    return templates.TemplateResponse(request, "areas/index.html", {
        "user": request.state.user
    })

@app.get("/areas/lista", response_class=HTMLResponse)
async def list_areas(request: Request, db: Session = Depends(get_db)):
    controller = AreasController(session=db)
    areas = controller.listar_areas()
    return templates.TemplateResponse(request, "areas/list.html", {
        "user": request.state.user,
        "areas": areas
    })

@app.post("/areas/crear")
async def create_area(request: Request, nombre: str = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(session=db)
    exito, mensaje = controller.crear_area(nombre, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/areas/actualizar")
async def update_area(request: Request, id: int = Form(...), nombre: str = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(session=db)
    exito, mensaje = controller.actualizar_area(id, nombre, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/areas/eliminar")
async def delete_area(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(session=db)
    exito, mensaje = controller.eliminar_area(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/salones", response_class=HTMLResponse)
async def view_salones(request: Request):
    return templates.TemplateResponse(request, "salones/index.html", {
        "user": request.state.user
    })

@app.get("/salones/lista", response_class=HTMLResponse)
async def list_salones(request: Request, db: Session = Depends(get_db)):
    controller = SalonesController(session=db)
    salones = controller.listar_salones()
    return templates.TemplateResponse(request, "salones/list.html", {
        "user": request.state.user,
        "salones": salones
    })

@app.post("/salones/crear")
async def create_salon(request: Request, nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(session=db)
    exito, mensaje = controller.crear_salon(nombre, edad, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/salones/actualizar")
async def update_salon(request: Request, id: int = Form(...), nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(session=db)
    exito, mensaje = controller.actualizar_salon(id, nombre, edad, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/salones/eliminar")
async def delete_salon(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(session=db)
    exito, mensaje = controller.eliminar_salon(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/aulas", response_class=HTMLResponse)
async def view_aulas(request: Request, db: Session = Depends(get_db)):
    # Necesitamos los salones para el selector del formulario
    controller = AulasController(session=db)
    salones = controller.listar_salones()
    return templates.TemplateResponse(request, "aulas/index.html", {
        "user": request.state.user,
        "salones": salones
    })

@app.get("/aulas/lista", response_class=HTMLResponse)
async def list_aulas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = AulasController(session=db)
    aulas = controller.listar_aulas_por_fecha(fecha)
    return templates.TemplateResponse(request, "aulas/list.html", {
        "user": request.state.user,
        "aulas": aulas,
        "fecha_filtro": fecha
    })

@app.post("/aulas/crear")
async def create_aula(
    request: Request,
    id_salon: int = Form(...),
    fecha: str = Form(...),
    maestra: int = Form(...),
    auxiliar: int = Form(...),
    capitan: int = Form(...),
    subcapitan: int = Form(...),
    colaborador: int = Form(...),
    ninos: int = Form(...),
    ninas: int = Form(...),
    condicion: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = AulasController(session=db)
    datos = {
        "id_salon": id_salon, "fecha": fecha, "maestra": maestra,
        "auxiliar": auxiliar, "capitan": capitan, "subcapitan": subcapitan,
        "colaborador": colaborador, "ninos": ninos, "ninas": ninas, "condicion": condicion
    }
    exito, mensaje = controller.crear_aula(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/aulas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/aulas/actualizar")
async def update_aula(
    request: Request,
    id: int = Form(...),
    id_salon: int = Form(...),
    fecha: str = Form(...),
    maestra: int = Form(...),
    auxiliar: int = Form(...),
    capitan: int = Form(...),
    subcapitan: int = Form(...),
    colaborador: int = Form(...),
    ninos: int = Form(...),
    ninas: int = Form(...),
    condicion: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = AulasController(session=db)
    datos = {
        "id_salon": id_salon, "fecha": fecha, "maestra": maestra,
        "auxiliar": auxiliar, "capitan": capitan, "subcapitan": subcapitan,
        "colaborador": colaborador, "ninos": ninos, "ninas": ninas, "condicion": condicion
    }
    exito, mensaje = controller.actualizar_aula(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/aulas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/aulas/eliminar")
async def delete_aula(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = AulasController(session=db)
    exito, mensaje = controller.eliminar_aula(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/aulas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/recepciones", response_class=HTMLResponse)
async def view_recepciones(request: Request):
    return templates.TemplateResponse(request, "recepciones/index.html", {
        "user": request.state.user
    })

@app.get("/recepciones/lista", response_class=HTMLResponse)
async def list_recepciones(request: Request, db: Session = Depends(get_db)):
    controller = RecepcionController(session=db)
    recepciones = controller.listar_recepciones()
    return templates.TemplateResponse(request, "recepciones/list.html", {
        "user": request.state.user,
        "recepciones": recepciones
    })

@app.post("/recepciones/crear")
async def create_recepcion(request: Request, nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(session=db)
    exito, mensaje = controller.crear_recepcion(nombre, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/recepciones/actualizar")
async def update_recepcion(request: Request, id: int = Form(...), nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(session=db)
    exito, mensaje = controller.actualizar_recepcion(id, nombre, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/recepciones/eliminar")
async def delete_recepcion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(session=db)
    exito, mensaje = controller.eliminar_recepcion(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/ensenanza", response_class=HTMLResponse)
async def view_ensenanza(request: Request):
    return templates.TemplateResponse(request, "ensenanza/index.html", {
        "user": request.state.user
    })

@app.get("/ensenanza/lista", response_class=HTMLResponse)
async def list_ensenanza(request: Request, db: Session = Depends(get_db)):
    controller = EnsenanzaController(session=db)
    registros = controller.listar_ensenanzas()
    return templates.TemplateResponse(request, "ensenanza/list.html", {
        "user": request.state.user,
        "registros": registros
    })

@app.post("/ensenanza/crear")
async def create_ensenanza(request: Request, capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(session=db)
    exito, mensaje = controller.crear_ensenanza(capitan, fecha, subcapitan, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/ensenanza/actualizar")
async def update_ensenanza(request: Request, id: int = Form(...), capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(session=db)
    exito, mensaje = controller.actualizar_ensenanza(id, capitan, subcapitan, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/ensenanza/eliminar")
async def delete_ensenanza(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(session=db)
    exito, mensaje = controller.eliminar_ensenanza(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logistica", response_class=HTMLResponse)
async def view_logistica(request: Request):
    return templates.TemplateResponse(request, "logistica/index.html", {
        "user": request.state.user
    })

@app.get("/logistica/lista", response_class=HTMLResponse)
async def list_logistica(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = LogisticaController(session=db)
    logisticas = controller.listar_logisticas(fecha=fecha)
    return templates.TemplateResponse(request, "logistica/list.html", {
        "user": request.state.user,
        "logisticas": logisticas,
        "fecha_filtro": fecha
    })

@app.post("/logistica/crear")
async def create_logistica(
    request: Request,
    almacen: str = Form(...),
    capitan: str = Form(...),
    distribucion: str = Form(None),
    hidratacion: str = Form(None),
    pasillo: str = Form(None),
    secretaria: str = Form(None),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = LogisticaController(session=db)
    datos = {
        "almacen": almacen, "capitan": capitan, "distribucion": distribucion,
        "hidratacion": hidratacion, "pasillo": pasillo, "secretaria": secretaria,
        "fecha": fecha
    }
    exito, mensaje = controller.crear_logistica(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/logistica?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/logistica/actualizar")
async def update_logistica(
    request: Request,
    id: int = Form(...),
    almacen: str = Form(...),
    capitan: str = Form(...),
    distribucion: str = Form(None),
    hidratacion: str = Form(None),
    pasillo: str = Form(None),
    secretaria: str = Form(None),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = LogisticaController(session=db)
    datos = {
        "almacen": almacen, "capitan": capitan, "distribucion": distribucion,
        "hidratacion": hidratacion, "pasillo": pasillo, "secretaria": secretaria,
        "fecha": fecha
    }
    exito, mensaje = controller.actualizar_logistica(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/logistica?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/logistica/eliminar")
async def delete_logistica(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = LogisticaController(session=db)
    exito, mensaje = controller.eliminar_logistica(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/logistica?msg={mensaje}&type={'success' if xito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/otras_areas", response_class=HTMLResponse)
async def view_otrasareas(request: Request):
    return templates.TemplateResponse(request, "otrasareas/index.html", {
        "user": request.state.user
    })

@app.get("/otras_areas/lista", response_class=HTMLResponse)
async def list_otrasareas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = OtrasAreasController(session=db)
    registros = controller.listar_otrasareas(fecha=fecha)
    return templates.TemplateResponse(request, "otrasareas/list.html", {
        "user": request.state.user,
        "registros": registros,
        "fecha_filtro": fecha
    })

@app.post("/otras_areas/crear")
async def create_otrasareas(
    request: Request,
    alabanza: int = Form(0), protocolo: int = Form(0), semillitas: int = Form(0),
    sonido: int = Form(0), teatro: int = Form(0), tv: int = Form(0),
    ujier: int = Form(0), seguridad: int = Form(0), fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = OtrasAreasController(session=db)
    datos = {
        "alabanza": alabanza, "protocolo": protocolo, "semillitas": semillitas,
        "sonido": sonido, "teatro": teatro, "tv": tv,
        "ujier": ujier, "seguridad": seguridad, "fecha": fecha
    }
    exito, mensaje = controller.crear_otrasareas(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/otras_areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/otras_areas/actualizar")
async def update_otrasareas(
    request: Request,
    id: int = Form(...),
    alabanza: int = Form(0), protocolo: int = Form(0), semillitas: int = Form(0),
    sonido: int = Form(0), teatro: int = Form(0), tv: int = Form(0),
    ujier: int = Form(0), seguridad: int = Form(0), fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = OtrasAreasController(session=db)
    datos = {
        "alabanza": alabanza, "protocolo": protocolo, "semillitas": semillitas,
        "sonido": sonido, "teatro": teatro, "tv": tv,
        "ujier": ujier, "seguridad": seguridad, "fecha": fecha
    }
    exito, mensaje = controller.actualizar_otrasareas(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/otras_areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/otras_areas/eliminar")
async def delete_otrasareas(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = OtrasAreasController(session=db)
    exito, mensaje = controller.eliminar_otrasareas(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/otras_areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/reportes", response_class=HTMLResponse)
async def view_reportes(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    resumen_texto = "Seleccione una fecha y genere el resumen."
    
    if fecha:
        try:
            servicio = ReporteEstadisticoService(db)
            resumen_data = servicio.obtener_resumen(fecha)
            resumen_texto = servicio.formatear_vista_previa(resumen_data)
        except Exception as e:
            logger.error(f"Error al generar resumen para la web: {e}")
            resumen_texto = f"Error al generar resumen: {e}"

    return templates.TemplateResponse(request, "reportes/index.html", {
        "user": request.state.user,
        "fecha_filtro": fecha,
        "resumen_texto": resumen_texto
    })

@app.post("/reportes/generar-pdf")
async def generar_reporte_pdf(request: Request, fecha: str = Form(...), db: Session = Depends(get_db)):
    if not fecha:
        raise HTTPException(status_code=400, detail="Debe seleccionar una fecha para generar el PDF.")
    
    try:
        servicio = ReporteEstadisticoService(db)
        resumen = servicio.obtener_resumen(fecha)
        graficos = servicio.generar_graficos(resumen)
        pdf_file_path = servicio.generar_pdf(resumen, graficos)
        
        return FileResponse(
            path=pdf_file_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_file_path)
        )
    except ModuleNotFoundError as e:
        logger.error(f"Error: {e}. Reportlab no está instalado.")
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {e}. Asegúrese de que reportlab esté instalado.")
    except Exception as e:
        logger.error(f"Error al generar PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {e}")

@app.get("/ayuda", response_class=HTMLResponse)
async def view_ayuda(request: Request):
    return templates.TemplateResponse(request, "ayudas/index.html", {
        "user": request.state.user
    })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("id_token")
    response.delete_cookie("local_id")
    response.delete_cookie("email")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_web:app", host="0.0.0.0", port=8000, reload=True)
