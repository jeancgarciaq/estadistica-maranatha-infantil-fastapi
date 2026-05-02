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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        # Intentar iniciar sesión en Firebase
        session_data = auth_service.sign_in(username, password)
        
        # En una aplicación real, usaríamos cookies de sesión o JWT.
        # Por ahora, simularemos una redirección exitosa.
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        # Podríamos guardar el token en una cookie (esto es simplificado)
        response.set_cookie(key="id_token", value=session_data.id_token)
        return response
    except Exception as e:
        logger.error("Error de login: %s", e)
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Credenciales inválidas o error de conexión."
        })

@app.get("/donaciones", response_class=HTMLResponse)
async def listar_donaciones_web(request: Request, db: Session = Depends(get_db)):
    controller = DonacionesController(session=db)
    donaciones = controller.listar_donaciones()
    return templates.TemplateResponse("donaciones/index.html", {
        "request": request,
        "donaciones": donaciones
    })

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("id_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_web:app", host="0.0.0.0", port=8000, reload=True)
