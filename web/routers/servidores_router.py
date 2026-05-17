from fastapi import APIRouter, Request, Depends, Form, Query
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.servidores_handler import ServidoresWebHandler
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(prefix="/servidores", tags=["Servidores"])
templates = Jinja2Templates(directory="web/templates")

@router.get("/")
async def view_servidores(request: Request, db: Session = Depends(get_db)):
    handler = ServidoresWebHandler(db, templates)
    return await handler.get_index(request)

@router.get("/lista")
async def list_servidores(
    request: Request, 
    nombre: Optional[str] = None, cedula: Optional[int] = None,
    area_servicio: Optional[str] = None, db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    filtros = {"nombre": nombre, "cedula": cedula, "area_servicio": area_servicio}
    return await handler.get_list(request, filtros)

@router.post("/crear")
async def create_servidor(
    request: Request, nombre: str = Form(...), edad: int = Form(...),
    cedula: int = Form(...), id_area: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    datos = {"nombre": nombre, "edad": edad, "cedula": cedula, "id_area": id_area}
    return await handler.post_crear(request, datos)

@router.post("/actualizar")
async def update_servidor(
    request: Request, id: int = Form(...), nombre: str = Form(...),
    cedula: int = Form(...), db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    datos = {"nombre": nombre, "cedula": cedula}
    return await handler.post_actualizar(request, id, datos)

@router.post("/eliminar")
async def delete_servidor(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    handler = ServidoresWebHandler(db, templates)
    return await handler.post_eliminar(request, id)

@router.get("/exportar")
async def export_servidores(
    request: Request, formato: str = "pdf", 
    nombre: Optional[str] = None, db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    return await handler.exportar(request, formato, {"nombre": nombre})