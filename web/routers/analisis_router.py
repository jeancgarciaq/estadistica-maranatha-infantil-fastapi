from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.analisis_handler import AnalisisWebHandler
from web.utils import get_current_user, templates

router = APIRouter()

def get_handler(db: Session = Depends(get_db)):
    return AnalisisWebHandler(db, templates)

@router.get("/analisis", response_class=HTMLResponse)
async def view_analisis(
    request: Request, 
    user=Depends(get_current_user), 
    handler: AnalisisWebHandler = Depends(get_handler)
):
    # Verificación estricta de seguridad: Solo ROOT
    if not user or user.rol.nombre != 'root':
        return RedirectResponse(url="/dashboard?error=No+tiene+permiso+para+acceder+a+esta+seccion")

    return await handler.get_analisis_index(request)