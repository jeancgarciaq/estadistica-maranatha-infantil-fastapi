import os
import logging
import json
import asyncio # Added for potential sleep in lifespan
import contextlib
import random
from functools import lru_cache
from typing import Optional

# 1. CARGAR VARIABLES DE ENTORNO ANTES QUE CUALQUIER OTRA COSA
from utils.env_loader import load_app_env
load_app_env()

# 2. IMPORTACIONES DE FASTAPI
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload

from models.database import get_db, configure_database, SessionLocal, shutdown_db
from utils.config_loader import obtener_medidas
from models.security import ROLE_ROOT, ROLE_LIMITS, Usuario, Rol

from controllers.areas_controller import AreasController
from controllers.aulas_controller import AulasController
from controllers.salones_controller import SalonesController
from controllers.donaciones_controller import DonacionesController
from controllers.usuarios_controller import UsuariosController
from controllers.ensenanza_controller import EnsenanzaController
from utils.reporte_estadistico import ReporteEstadisticoService
from controllers.otras_areas_controller import OtrasAreasController
from controllers.recepcion_controller import RecepcionController
from controllers.logistica_controller import LogisticaController
from controllers.distribucion_controller import DistribucionesController
from controllers.servidor_controller import ServidorController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Ejecutar al iniciar: Crear tablas y sembrar datos
    configure_database()
    yield
    # Ejecutar al apagar: Cerrar conector de Cloud SQL
    await asyncio.sleep(0.1) # Give aiohttp a moment to clean up
    shutdown_db()

# Inicializar FastAPI
app = FastAPI(title="Estadística Maranatha Kids - Web", lifespan=lifespan)
security = HTTPBearer()

@lru_cache(maxsize=32)
def obtener_usuario_cache(db: Session, username: str):
    """Cache simple para evitar consultas repetitivas a Cloud SQL en cada request."""
    return (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.username == username, Usuario.activo == True)
        .first()
    )

templates = Jinja2Templates(directory="web/templates")

# Middleware de Autenticación y Autorización
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    public_paths = ["/login", "/logout", "/api/config/medidas", "/register", "/forgot-password", "/reset-password"]
    
    if request.url.path == "/" or any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Obtener usuario de la cookie de sesión local
    username = request.cookies.get("session_user")

    if not username:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    db = SessionLocal()
    try:
        user = obtener_usuario_cache(db, username)
        if not user:
            raise Exception("Usuario no encontrado o inactivo")
        request.state.user = user
        # Continuamos con el resto de la aplicación
        return await call_next(request)
    except Exception as e:
        logger.error(f"Error de autenticación en middleware: {e}")
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("session_user")
        return response
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    controller = UsuariosController(db)
    exito, usuario, mensaje = controller.autenticar(username, password)
    
    if exito:
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        # Establecer cookie de sesión (en producción usar JWT o cookies firmadas)
        response.set_cookie(key="session_user", value=usuario.username, httponly=True)
        return response
    else:
        return templates.TemplateResponse(request, "login.html", {"error": mensaje})

@app.get("/register", response_class=HTMLResponse)
async def register_view(request: Request, db: Session = Depends(get_db)):
    controller = UsuariosController(db)
    roles = controller.listar_roles()
    # Generamos números aleatorios para el desafío
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return templates.TemplateResponse(request, "register.html", {
        "roles": roles,
        "math_challenge": f"¿Cuánto es {num1} + {num2}?",
        "math_result": num1 + num2
    })

@app.post("/register")
async def register_post(
    request: Request,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    rol_nombre: Optional[str] = Form(None),
    math_answer: Optional[int] = Form(None),
    math_expected: Optional[int] = Form(None),
    website: str = Form(None), # Campo Honeypot
    db: Session = Depends(get_db)
):
    controller = UsuariosController(db)
    # Regeneramos el desafío en caso de error para que no sea estático
    num1_err = random.randint(1, 10)
    num2_err = random.randint(1, 10)
    # Validación de campos obligatorios para evitar el JSON de error
    if not all([username, password, rol_nombre, math_answer is not None]):
        return templates.TemplateResponse(request, "register.html", {
            "error": "Todos los campos son obligatorios.",
            "roles": controller.listar_roles(),
            "math_challenge": f"¿Cuánto es {num1_err} + {num2_err}?",
            "math_result": num1_err + num2_err
        })

    if math_answer != math_expected:
        return templates.TemplateResponse(request, "register.html", {
            "error": "Respuesta matemática incorrecta.",
            "roles": controller.listar_roles(),
            "math_challenge": f"¿Cuánto es {num1_err} + {num2_err}?",
            "math_result": num1_err + num2_err
        })

    datos = {
        "username": username,
        "password": password,
        "rol_nombre": rol_nombre,
        "website": website
    }
    
    exito, mensaje = controller.registrar_usuario(datos)
    if exito:
        return RedirectResponse(url="/?msg=Registro exitoso. Ya puede iniciar sesión.", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "register.html", {
        "error": mensaje, 
        "roles": controller.listar_roles(),
        "math_challenge": f"¿Cuánto es {num1_err} + {num2_err}?",
        "math_result": num1_err + num2_err
    })

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_view(request: Request):
    return templates.TemplateResponse(request, "forgot_password.html")

@app.post("/forgot-password")
async def forgot_password_post(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    controller = UsuariosController(db)
    exito, mensaje = controller.solicitar_restablecimiento_contrasena(email)
    if exito:
        return templates.TemplateResponse(request, "forgot_password.html", {
            "message": mensaje,
            "email_sent": True
        })
    return templates.TemplateResponse(request, "forgot_password.html", {"error": mensaje})

@app.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_view(request: Request, token: str, db: Session = Depends(get_db)):
    controller = UsuariosController(db)
    usuario = controller.validar_token_restablecimiento(token)
    if not usuario:
        return templates.TemplateResponse(request, "reset_password.html", {
            "error": "El enlace de restablecimiento es inválido o ha expirado."
        })
    return templates.TemplateResponse(request, "reset_password.html", {
        "token": token,
        "username": usuario.username
    })

@app.post("/reset-password/{token}")
async def reset_password_post(
    request: Request,
    token: str,
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        return templates.TemplateResponse(request, "reset_password.html", {
            "token": token,
            "error": "Las contraseñas no coinciden."
        })
    controller = UsuariosController(db)
    exito, mensaje = controller.restablecer_contrasena(token, password)
    if exito:
        return RedirectResponse(url="/?msg=Contraseña restablecida exitosamente. Ya puede iniciar sesión.&type=success", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "reset_password.html", {"token": token, "error": mensaje})

@app.get("/usuarios", response_class=HTMLResponse)
async def view_usuarios(request: Request, db: Session = Depends(get_db)):
    if request.state.user.rol.nombre != ROLE_ROOT:
        return RedirectResponse(url="/dashboard?msg=Acceso restringido al superusuario&type=error", status_code=status.HTTP_303_SEE_OTHER)
    
    controller = UsuariosController(db)
    roles = controller.listar_roles()
    return templates.TemplateResponse(request, "usuarios/index.html", {
        "user": request.state.user,
        "roles": roles
    })

@app.get("/usuarios/lista", response_class=HTMLResponse)
async def list_usuarios(request: Request, db: Session = Depends(get_db)):
    if request.state.user.rol.nombre != ROLE_ROOT:
        return HTMLResponse("Acceso denegado", status_code=status.HTTP_403_FORBIDDEN)
    
    controller = UsuariosController(db)
    usuarios = controller.listar_usuarios()
    return templates.TemplateResponse(request, "usuarios/list.html", {
        "usuarios": usuarios,
        "user": request.state.user
    })

@app.post("/usuarios/crear")
async def create_usuario(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    rol_nombre: str = Form(...),
    db: Session = Depends(get_db)
):
    if request.state.user.rol.nombre != ROLE_ROOT:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    controller = UsuariosController(db)
    exito, mensaje = controller.registrar_usuario({"username": username, "password": password, "rol_nombre": rol_nombre}, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/usuarios?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/usuarios/actualizar")
async def update_usuario(
    request: Request,
    id: int = Form(...),
    password: str = Form(None),
    rol_nombre: str = Form(None),
    activo: str = Form(None),
    db: Session = Depends(get_db)
):
    if request.state.user.rol.nombre != ROLE_ROOT:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    controller = UsuariosController(db)
    is_active = True if activo == "on" else False
    
    exito, mensaje = controller.actualizar_usuario(
        user_id=id, password=password, rol_nombre=rol_nombre, activo=is_active, 
        user_context={"user": request.state.user}
    )
    return RedirectResponse(url=f"/usuarios?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/servidores", response_class=HTMLResponse)
async def view_servidores(request: Request):
    # Restricción de acceso: Solo root y administrador
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.view"):
        return RedirectResponse(url="/dashboard?msg=Acceso restringido&type=error", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(request, "servidores/index.html", {
        "user": request.state.user
    })

@app.get("/servidores/lista", response_class=HTMLResponse)
async def list_servidores(
    request: Request, 
    nombre: Optional[str] = None,
    cedula: Optional[int] = None,
    celular: Optional[str] = None,
    correo: Optional[str] = None,
    area_servicio: Optional[str] = None,
    mes_nacimiento: Optional[int] = None,
    dia_nacimiento: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.view"):
        return HTMLResponse("Acceso denegado", status_code=status.HTTP_403_FORBIDDEN)
    
    filtros = {
        "nombre": nombre, "cedula": cedula, "celular": celular, "correo": correo, 
        "area_servicio": area_servicio, "mes_nacimiento": mes_nacimiento, "dia_nacimiento": dia_nacimiento
    }
    controller = ServidorController(db)
    servidores = controller.listar_servidores(filtros=filtros)
    return templates.TemplateResponse(request, "servidores/list.html", {
        "servidores": servidores,
        "user": request.state.user
    })

@app.post("/servidores/crear")
async def create_servidor(
    request: Request,
    nombre: str = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    cedula: int = Form(...),
    celular: str = Form(None),
    correo: str = Form(None),
    numero_equipo: int = Form(None),
    area_servicio: str = Form(None),
    capitan: str = Form(None),
    db: Session = Depends(get_db)
):
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
        return RedirectResponse(url="/servidores?msg=No tiene permisos para crear&type=error", status_code=status.HTTP_303_SEE_OTHER)
    
    controller = ServidorController(db)
    datos = {
        "nombre": nombre, "edad": edad, "fecha_nacimiento": fecha_nacimiento, "cedula": cedula, "celular": celular,
        "correo": correo, "numero_equipo": numero_equipo, 
        "area_servicio": area_servicio, "capitan": capitan
    }
    exito, mensaje = controller.crear_servidor(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/servidores?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/servidores/actualizar")
async def update_servidor(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    cedula: int = Form(...),
    celular: str = Form(None),
    correo: str = Form(None),
    numero_equipo: int = Form(None),
    area_servicio: str = Form(None),
    capitan: str = Form(None),
    db: Session = Depends(get_db)
):
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
        return RedirectResponse(url="/servidores?msg=No tiene permisos para editar&type=error", status_code=status.HTTP_303_SEE_OTHER)

    controller = ServidorController(db)
    datos = {
        "nombre": nombre, "edad": edad, "fecha_nacimiento": fecha_nacimiento, "cedula": cedula, "celular": celular,
        "correo": correo, "numero_equipo": numero_equipo, 
        "area_servicio": area_servicio, "capitan": capitan
    }
    exito, mensaje = controller.actualizar_servidor(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/servidores?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/servidores/eliminar")
async def delete_servidor(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.manage"):
        return RedirectResponse(url="/servidores?msg=No tiene permisos para eliminar&type=error", status_code=status.HTTP_303_SEE_OTHER)

    controller = ServidorController(db)
    exito, mensaje = controller.eliminar_servidor(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/servidores?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/servidores/exportar")
async def export_servidores(
    request: Request,
    formato: str = "pdf",
    nombre: Optional[str] = None,
    cedula: Optional[int] = None,
    celular: Optional[str] = None,
    correo: Optional[str] = None,
    area_servicio: Optional[str] = None,
    mes_nacimiento: Optional[int] = None,
    dia_nacimiento: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not UsuariosController.usuario_tiene_permiso(request.state.user, "servidores.view"):
        raise HTTPException(status_code=403, detail="Acceso denegado")

    filtros = {
        "nombre": nombre, "cedula": cedula, "celular": celular, "correo": correo, 
        "area_servicio": area_servicio, "mes_nacimiento": mes_nacimiento, "dia_nacimiento": dia_nacimiento
    }
    controller = ServidorController(db)
    servidores = controller.listar_servidores(filtros=filtros)

    if formato == "pdf":
        pdf_content = controller.generar_reporte_pdf(servidores)
        headers = {"Content-Disposition": "attachment; filename=servidores.pdf"}
        return Response(content=pdf_content, media_type="application/pdf", headers=headers)

    if formato == "excel":
        excel_content = controller.generar_reporte_excel(servidores)
        headers = {"Content-Disposition": "attachment; filename=servidores_export.xlsx"}
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return Response(content=excel_content, media_type=content_type, headers=headers)

    return RedirectResponse(url="/servidores?msg=Formato no soportado&type=error")

@app.get("/donaciones", response_class=HTMLResponse)
async def view_donaciones(request: Request):
    medidas = obtener_medidas()
    return templates.TemplateResponse(request, "donaciones/index.html", {
        "user": request.state.user,
        "medidas": medidas
    })

@app.get("/donaciones/lista", response_class=HTMLResponse)
async def list_donaciones(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = DonacionesController(db)
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
    controller = DonacionesController(db)
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
    controller = DonacionesController(db)
    datos = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    exito, mensaje = controller.actualizar_donacion(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/donaciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/donaciones/eliminar")
async def delete_donacion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = DonacionesController(db)
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
    controller = DonacionesController(db)
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
    controller = DonacionesController(db)
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
    controller = DistribucionesController(db)
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
    controller = DistribucionesController(db)
    datos = {
        "donacion_id": donacion_id, "alimento_preparado_id": alimento_preparado_id,
        "salon_id": salon_id, "area_id": area_id, "recepcion_id": recepcion_id,
        "cantidad": cantidad, "unidad": unidad, "fecha": fecha
    }
    exito, mensaje = controller.crear_distribucion(datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/distribuciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/distribuciones/eliminar")
async def delete_distribucion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = DistribucionesController(db)
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
    controller = AreasController(db)
    areas = controller.listar_areas()
    return templates.TemplateResponse(request, "areas/list.html", {
        "user": request.state.user,
        "areas": areas
    })

@app.post("/areas/crear")
async def create_area(request: Request, nombre: str = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(db)
    exito, mensaje = controller.crear_area(nombre, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/areas/actualizar")
async def update_area(request: Request, id: int = Form(...), nombre: str = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(db)
    exito, mensaje = controller.actualizar_area(id, nombre, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/areas/eliminar")
async def delete_area(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = AreasController(db)
    exito, mensaje = controller.eliminar_area(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/salones", response_class=HTMLResponse)
async def view_salones(request: Request):
    return templates.TemplateResponse(request, "salones/index.html", {
        "user": request.state.user
    })

@app.get("/salones/lista", response_class=HTMLResponse)
async def list_salones(request: Request, db: Session = Depends(get_db)):
    controller = SalonesController(db)
    salones = controller.listar_salones()
    return templates.TemplateResponse(request, "salones/list.html", {
        "user": request.state.user,
        "salones": salones
    })

@app.post("/salones/crear")
async def create_salon(request: Request, nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(db)
    exito, mensaje = controller.crear_salon(nombre, edad, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/salones/actualizar")
async def update_salon(request: Request, id: int = Form(...), nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(db)
    exito, mensaje = controller.actualizar_salon(id, nombre, edad, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/salones/eliminar")
async def delete_salon(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = SalonesController(db)
    exito, mensaje = controller.eliminar_salon(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/salones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/aulas", response_class=HTMLResponse)
async def view_aulas(request: Request, db: Session = Depends(get_db)):
    # Necesitamos los salones para el selector del formulario
    controller = AulasController(db)
    salones = controller.listar_salones()
    return templates.TemplateResponse(request, "aulas/index.html", {
        "user": request.state.user,
        "salones": salones
    })

@app.get("/aulas/lista", response_class=HTMLResponse)
async def list_aulas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = AulasController(db)
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
    controller = AulasController(db)
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
    controller = AulasController(db)
    datos = {
        "id_salon": id_salon, "fecha": fecha, "maestra": maestra,
        "auxiliar": auxiliar, "capitan": capitan, "subcapitan": subcapitan,
        "colaborador": colaborador, "ninos": ninos, "ninas": ninas, "condicion": condicion
    }
    exito, mensaje = controller.actualizar_aula(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/aulas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/aulas/eliminar")
async def delete_aula(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = AulasController(db)
    exito, mensaje = controller.eliminar_aula(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/aulas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/recepciones", response_class=HTMLResponse)
async def view_recepciones(request: Request):
    return templates.TemplateResponse(request, "recepciones/index.html", {
        "user": request.state.user
    })

@app.get("/recepciones/lista", response_class=HTMLResponse)
async def list_recepciones(request: Request, db: Session = Depends(get_db)):
    controller = RecepcionController(db)
    recepciones = controller.listar_recepciones()
    return templates.TemplateResponse(request, "recepciones/list.html", {
        "user": request.state.user,
        "recepciones": recepciones
    })

@app.post("/recepciones/crear")
async def create_recepcion(request: Request, nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(db)
    exito, mensaje = controller.crear_recepcion(nombre, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/recepciones/actualizar")
async def update_recepcion(request: Request, id: int = Form(...), nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(db)
    exito, mensaje = controller.actualizar_recepcion(id, nombre, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/recepciones/eliminar")
async def delete_recepcion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = RecepcionController(db)
    exito, mensaje = controller.eliminar_recepcion(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/recepciones?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/ensenanza", response_class=HTMLResponse)
async def view_ensenanza(request: Request):
    return templates.TemplateResponse(request, "ensenanza/index.html", {
        "user": request.state.user
    })

@app.get("/ensenanza/lista", response_class=HTMLResponse)
async def list_ensenanza(request: Request, db: Session = Depends(get_db)):
    controller = EnsenanzaController(db)
    registros = controller.listar_ensenanzas()
    return templates.TemplateResponse(request, "ensenanza/list.html", {
        "user": request.state.user,
        "registros": registros
    })

@app.post("/ensenanza/crear")
async def create_ensenanza(request: Request, capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(db)
    exito, mensaje = controller.crear_ensenanza(capitan, fecha, subcapitan, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/ensenanza/actualizar")
async def update_ensenanza(request: Request, id: int = Form(...), capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(db)
    exito, mensaje = controller.actualizar_ensenanza(id, capitan, subcapitan, fecha, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/ensenanza/eliminar")
async def delete_ensenanza(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = EnsenanzaController(db)
    exito, mensaje = controller.eliminar_ensenanza(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/ensenanza?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logistica", response_class=HTMLResponse)
async def view_logistica(request: Request):
    return templates.TemplateResponse(request, "logistica/index.html", {
        "user": request.state.user
    })

@app.get("/logistica/lista", response_class=HTMLResponse)
async def list_logistica(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = LogisticaController(db)
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
    capitan: int = Form(...),
    distribucion: int = Form(0),
    hidratacion: int = Form(0),
    pasillo: int = Form(0),
    secretaria: int = Form(0),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = LogisticaController(db)
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
    almacen: int = Form(...),
    capitan: int = Form(...),
    distribucion: int = Form(0),
    hidratacion: int = Form(0),
    pasillo: int = Form(0),
    secretaria: int = Form(0),
    fecha: str = Form(...),
    db: Session = Depends(get_db)
):
    controller = LogisticaController(db)
    datos = {
        "almacen": almacen, "capitan": capitan, "distribucion": distribucion,
        "hidratacion": hidratacion, "pasillo": pasillo, "secretaria": secretaria,
        "fecha": fecha
    }
    exito, mensaje = controller.actualizar_logistica(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/logistica?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/logistica/eliminar")
async def delete_logistica(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = LogisticaController(db)
    exito, mensaje = controller.eliminar_logistica(id, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/logistica?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/otras_areas", response_class=HTMLResponse)
async def view_otrasareas(request: Request):
    return templates.TemplateResponse(request, "otrasareas/index.html", {
        "user": request.state.user
    })

@app.get("/otras_areas/lista", response_class=HTMLResponse)
async def list_otrasareas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    controller = OtrasAreasController(db)
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
    controller = OtrasAreasController(db)
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
    controller = OtrasAreasController(db)
    datos = {
        "alabanza": alabanza, "protocolo": protocolo, "semillitas": semillitas,
        "sonido": sonido, "teatro": teatro, "tv": tv,
        "ujier": ujier, "seguridad": seguridad, "fecha": fecha
    }
    exito, mensaje = controller.actualizar_otrasareas(id, datos, user_context={"user": request.state.user})
    return RedirectResponse(url=f"/otras_areas?msg={mensaje}&type={'success' if exito else 'error'}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/otras_areas/eliminar")
async def delete_otrasareas(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    controller = OtrasAreasController(db)
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
    response.delete_cookie("session_user")
    return response

if __name__ == "__main__":
    import uvicorn
    # Use the PORT env var set by Cloud Run (default 8080) and bind to 0.0.0.0
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    # Enable reload only in development environments
    reload_flag = os.environ.get("ENV", "").lower() in ("dev", "development")
    uvicorn.run("main_web:app", host=host, port=port, reload=reload_flag)
