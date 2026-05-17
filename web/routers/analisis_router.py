from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.analisis_handler import AnalisisWebHandler
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

@router.get("/analisis", response_class=HTMLResponse)
async def view_analisis(
    request: Request, 
    db: Session = Depends(get_db)
):
    handler = AnalisisWebHandler(db, templates)
    user = getattr(request.state, 'user', None)
    
    # Verificación estricta de seguridad: Solo ROOT
    if not user or user.rol.nombre != 'root':
        return RedirectResponse(url="/dashboard?error=No+tiene+permiso+para+acceder+a+esta+seccion")

    return await handler.get_analisis_index(request)