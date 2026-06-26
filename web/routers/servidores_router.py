from fastapi import APIRouter, Request, Depends, Form
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
    nombre: Optional[str] = None,
    cedula: Optional[int] = None,
    db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    filtros = {"nombre": nombre, "cedula": cedula}
    return await handler.get_list(request, filtros)

@router.post("/crear")
async def create_servidor(
    request: Request,
    nombre: str = Form(...),
    edad: int = Form(...),
    cedula: int = Form(...),
    celular: Optional[str] = Form(None),
    correo: Optional[str] = Form(None),
    numero_equipo: Optional[int] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    id_capitan: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    datos = {
        "nombre": nombre, "edad": edad, "cedula": cedula,
        "celular": celular, "correo": correo,
        "numero_equipo": numero_equipo,
        "fecha_nacimiento": fecha_nacimiento,
        "id_capitan": id_capitan
    }
    return await handler.post_crear(request, datos)

@router.post("/actualizar")
async def update_servidor(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    edad: int = Form(...),
    cedula: int = Form(...),
    celular: Optional[str] = Form(None),
    correo: Optional[str] = Form(None),
    numero_equipo: Optional[int] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    id_capitan: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    datos = {
        "nombre": nombre, "edad": edad, "cedula": cedula,
        "celular": celular, "correo": correo,
        "numero_equipo": numero_equipo,
        "fecha_nacimiento": fecha_nacimiento,
        "id_capitan": id_capitan
    }
    return await handler.post_actualizar(request, id, datos)

@router.post("/eliminar")
async def delete_servidor(
    request: Request,
    id: int = Form(...),
    db: Session = Depends(get_db)
):
    handler = ServidoresWebHandler(db, templates)
    return await handler.post_eliminar(request, id)
