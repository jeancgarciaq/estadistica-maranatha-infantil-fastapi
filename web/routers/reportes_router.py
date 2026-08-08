from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.reportes_handler import ReportesWebHandler
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/reportes", tags=["Reportes"])
templates = Jinja2Templates(directory="web/templates")
templates.env.globals["prefix"] = ""

@router.get("/")
async def view_reportes(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    handler = ReportesWebHandler(db, templates)
    return await handler.get_reportes_index(request, fecha)

@router.post("/generar-pdf")
async def generar_reporte_pdf(request: Request, fecha: str = Form(...), db: Session = Depends(get_db)):
    handler = ReportesWebHandler(db, templates)
    return await handler.post_generar_pdf(request, fecha)