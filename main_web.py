import os
import logging
import asyncio # Added for potential sleep in lifespan
import contextlib
import time

# 1. CARGAR VARIABLES DE ENTORNO ANTES QUE CUALQUIER OTRA COSA
from utils.env_loader import load_app_env
load_app_env()

# 2. CONFIGURAR LOGGING (consola + archivo logs/app.log)
from utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

# 2. IMPORTACIONES DE FASTAPI
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload

from models.database import configure_database, SessionLocal, shutdown_db
from models.security import ROLE_ROOT, Usuario, Rol

# Importar Routers Refactorizados
from web.routers import alimentos_router, auth_router, usuarios_router, jerarquia_router, infraestructura_router, reportes_router, ayuda_router, analisis_router, servidores_router

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando proceso de startup (lifespan)...")
    start_time = time.time()
    
    # Ejecutar configuración de base de datos
    configure_database()
    
    logger.info(f"✨ Startup completado en {time.time() - start_time:.2f} segundos.")
    yield
    # Ejecutar al apagar: Cerrar conector de Cloud SQL
    await asyncio.sleep(0.1) # Give aiohttp a moment to clean up
    shutdown_db()

# Inicializar FastAPI
app = FastAPI(title="Estadistica Maranatha Kids - Web", lifespan=lifespan)
security = HTTPBearer()

# Incluir Routers
app.include_router(alimentos_router.router)
app.include_router(auth_router.router)
app.include_router(usuarios_router.router)
app.include_router(jerarquia_router.router)
app.include_router(infraestructura_router.router)
app.include_router(reportes_router.router)
app.include_router(ayuda_router.router)
app.include_router(analisis_router.router)
app.include_router(servidores_router.router)

def obtener_usuario_cache(db: Session, username: str):
    """Obtiene el usuario con su rol y permisos cargados (sin cache).

    El @lru_cache anterior podía devolver un objeto ligado a una sesión ya
    cerrada, provocando el error 'Parent instance is not bound to a Session'.
    """
    return (
        db.query(Usuario)
        .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
        .filter(Usuario.username == username, Usuario.activo == True)
        .first()
    )

templates = Jinja2Templates(directory="web/templates")
PREFIX = ""
templates.env.globals["prefix"] = PREFIX

# Middleware de Autenticación y Autorización
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    public_paths = ["/login", "/logout", "/api/config/medidas", "/register", "/forgot-password", "/reset-password"]
    
    # Normalizar path para comparación
    request_path = request.url.path
    
    if request_path == "/" or any(request_path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Obtener usuario de la cookie de sesión local
    username = request.cookies.get("session_user")

    if not username:
        # Redirigir al login explícitamente, no a la raíz
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    db = SessionLocal()
    try:
        try:
            user = obtener_usuario_cache(db, username)
        except Exception as e:
            # Solo errores reales de autenticación/búsqueda del usuario
            logger.error(f"Error de sesión al autenticar '{username}': {e}", exc_info=True)
            response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
            response.delete_cookie("session_user")
            return response

        if not user:
            # Sesión inválida: limpiar cookie y volver al login
            response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
            response.delete_cookie("session_user")
            return response

        request.state.user = user
        # Mantener la sesión abierta durante el renderizado (permite lazy-load como user.rol.permisos).
        # Se cierra en el finally DESPUÉS de enviar la respuesta.
        return await call_next(request)
    finally:
        db.close()

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {
        "user": request.state.user
    })

if __name__ == "__main__":
    import uvicorn
    # Use the PORT env var set by Cloud Run (default 8080) and bind to 0.0.0.0
    port = int(os.environ.get("PORT", 8001))
    host = "0.0.0.0"
    # Enable reload only in development environments
    reload_flag = os.environ.get("ENV", "").lower() in ("dev", "development")
    uvicorn.run("main_web:app", host=host, port=port, reload=reload_flag)
