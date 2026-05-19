from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.usuarios_handler import UsuariosWebHandler
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
templates = Jinja2Templates(directory="web/templates")

@router.get("/")
async def view_usuarios(request: Request, db: Session = Depends(get_db)):
    handler = UsuariosWebHandler(db, templates)
    return await handler.get_index(request)

@router.get("/lista")
async def list_usuarios(request: Request, db: Session = Depends(get_db)):
    handler = UsuariosWebHandler(db, templates)
    return await handler.get_list(request)

@router.post("/crear")
async def create_usuario(
    request: Request, username: str = Form(...), password: str = Form(...),
    rol_nombre: str = Form(...), db: Session = Depends(get_db)
):
    handler = UsuariosWebHandler(db, templates)
    datos = {"username": username, "password": password, "rol_nombre": rol_nombre}
    return await handler.post_crear(request, datos)

@router.post("/actualizar")
async def update_usuario(
    request: Request, id: int = Form(...), password: Optional[str] = Form(None),
    rol_nombre: Optional[str] = Form(None), activo: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    handler = UsuariosWebHandler(db, templates)
    return await handler.post_actualizar(request, id, password, rol_nombre, activo)

@router.post("/eliminar")
async def delete_usuario(
    request: Request, id: int = Form(...), db: Session = Depends(get_db)
):
    handler = UsuariosWebHandler(db, templates)
    return await handler.post_eliminar(request, id)