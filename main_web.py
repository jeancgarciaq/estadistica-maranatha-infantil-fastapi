import os
import logging
import asyncio # Added for potential sleep in lifespan
import contextlib
import time
from functools import lru_cache

# 1. CARGAR VARIABLES DE ENTORNO ANTES QUE CUALQUIER OTRA COSA
from utils.env_loader import load_app_env
load_app_env()

# 2. IMPORTACIONES DE FASTAPI
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session, joinedload

from models.database import configure_database, SessionLocal, shutdown_db
from models.security import ROLE_ROOT, Usuario

# Importar Routers Refactorizados
from web.routers import alimentos_router, servidores_router, auth_router, usuarios_router, jerarquia_router, infraestructura_router, reportes_router, ayuda_router, analisis_router

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
app = FastAPI(title="Estadística Maranatha Kids - Web", lifespan=lifespan)
security = HTTPBearer()

# Incluir Routers
app.include_router(alimentos_router.router)
app.include_router(servidores_router.router)
app.include_router(auth_router.router)
app.include_router(usuarios_router.router)
app.include_router(jerarquia_router.router)
app.include_router(infraestructura_router.router)
app.include_router(reportes_router.router)
app.include_router(ayuda_router.router)
app.include_router(analisis_router.router)

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

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {
        "user": request.state.user
    })

if __name__ == "__main__":
    import uvicorn
    # Use the PORT env var set by Cloud Run (default 8080) and bind to 0.0.0.0
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    # Enable reload only in development environments
    reload_flag = os.environ.get("ENV", "").lower() in ("dev", "development")
    uvicorn.run("main_web:app", host=host, port=port, reload=reload_flag)
