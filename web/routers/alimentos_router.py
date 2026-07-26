from fastapi import APIRouter, Request, Depends, Form, status
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.alimentos_handler import AlimentosWebHandler
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(tags=["Alimentos"])
templates = Jinja2Templates(directory="web/templates")
templates.env.globals["prefix"] = "/semi"

def get_handler(db: Session = Depends(get_db)):
    return AlimentosWebHandler(db, templates)

# Rutas de Donaciones
@router.get("/donaciones")
async def view_donaciones(request: Request, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_donaciones_index(request)

@router.get("/donaciones/lista")
async def list_donaciones(request: Request, fecha: str = None, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_donaciones_list(request, fecha)

@router.post("/donaciones/crear")
async def create_donacion(request: Request, descripcion: str = Form(...), cantidad: float = Form(...), 
                         unidad: str = Form(...), fecha: str = Form(...), equipo: str = Form(...), 
                         handler: AlimentosWebHandler = Depends(get_handler)):
    datos = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    return await handler.post_donacion_crear(request, datos)

# Rutas de Preparados
@router.get("/preparados")
async def view_preparados(request: Request, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_preparados_index(request)

@router.get("/preparados/lista")
async def list_preparados(request: Request, fecha: str = None, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_preparados_list(request, fecha)

@router.post("/preparados/crear")
async def create_preparado(request: Request, descripcion: str = Form(...), cantidad: float = Form(...),
                          unidad: str = Form(...), fecha: str = Form(...), equipo: str = Form(...),
                          componentes_json: str = Form(...), handler: AlimentosWebHandler = Depends(get_handler)):
    datos_res = {"descripcion": descripcion, "cantidad": cantidad, "unidad": unidad, "fecha": fecha, "equipo": equipo}
    return await handler.post_preparado_crear(request, datos_res, componentes_json)

# Rutas de Distribuciones
@router.get("/distribuciones")
async def view_distribuciones(request: Request, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_distribuciones_index(request)

@router.get("/distribuciones/lista")
async def list_distribuciones(request: Request, fecha: str = None, handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.get_distribuciones_list(request, fecha)

@router.post("/distribuciones/crear")
async def create_distribucion(request: Request, donacion_id: Optional[int] = Form(None), 
                             alimento_preparado_id: Optional[int] = Form(None), salon_id: Optional[int] = Form(None),
                             area_id: Optional[int] = Form(None), recepcion_id: Optional[int] = Form(None),
                             cantidad: float = Form(...), unidad: str = Form(...), fecha: str = Form(...),
                             handler: AlimentosWebHandler = Depends(get_handler)):
    datos = {
        "donacion_id": donacion_id, "alimento_preparado_id": alimento_preparado_id,
        "salon_id": salon_id, "area_id": area_id, "recepcion_id": recepcion_id,
        "cantidad": cantidad, "unidad": unidad, "fecha": fecha
    }
    return await handler.post_distribucion_crear(request, datos)

@router.post("/distribuciones/eliminar")
async def delete_distribucion(request: Request, id: int = Form(...), handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.post_distribucion_eliminar(request, id)

# APIs
@router.get("/api/materias-primas")
async def get_materias_primas(handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.api_materias_primas()

@router.get("/api/config/medidas")
async def get_medidas(handler: AlimentosWebHandler = Depends(get_handler)):
    return await handler.api_medidas()