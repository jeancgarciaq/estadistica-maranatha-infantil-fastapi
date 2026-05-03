import os
import logging
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
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
    public_paths = ["/", "/login", "/logout", "/static", "/api/config/medidas"]
    if any(request.url.path.startswith(path) for path in public_paths) or request.url.path == "/":
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
    return templates.TemplateResponse("login.html", {"request": request})

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
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": str(e)
        })

@app.get("/donaciones", response_class=HTMLResponse)
async def listar_donaciones_web(request: Request, db: Session = Depends(get_db)):
    # El usuario ya está disponible en request.state.user gracias al middleware
    user = request.state.user
    controller = DonacionesController(session=db)
    donaciones = controller.listar_donaciones()
    
    return templates.TemplateResponse("donaciones/index.html", {
        "request": request,
        "donaciones": donaciones,
        "user": user
    })

@app.get("/api/config/medidas")
async def get_medidas():
    """Endpoint para que el frontend JS obtenga las unidades de medida para los select/dropdowns."""
    return {"unidades": obtener_medidas()}

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": request.state.user
    })

@app.get("/areas", response_class=HTMLResponse)
async def view_areas(request: Request):
    return templates.TemplateResponse("areas/index.html", {
        "request": request,
        "user": request.state.user
    })

@app.get("/areas/lista", response_class=HTMLResponse)
async def list_areas(request: Request, db: Session = Depends(get_db)):
    controller = AreasController(session=db)
    areas = controller.listar_areas()
    return templates.TemplateResponse("areas/list.html", {
        "request": request,
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
    return templates.TemplateResponse("salones/index.html", {
        "request": request,
        "user": request.state.user
    })

@app.get("/salones/lista", response_class=HTMLResponse)
async def list_salones(request: Request, db: Session = Depends(get_db)):
    controller = SalonesController(session=db)
    salones = controller.listar_salones()
    return templates.TemplateResponse("salones/list.html", {
        "request": request,
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
    return templates.TemplateResponse("aulas/index.html", {
        "request": request,
        "user": request.state.user,
        "salones": salones
    })

@app.get("/aulas/lista", response_class=HTMLResponse)
async def list_aulas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = AulasController(session=db)
    aulas = controller.listar_aulas_por_fecha(fecha)
    return templates.TemplateResponse("aulas/list.html", {
        "request": request,
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
