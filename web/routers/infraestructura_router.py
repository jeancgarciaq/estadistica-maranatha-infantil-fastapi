from fastapi import APIRouter, Request, Depends, Form, status, Query
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.infraestructura_handler import InfraestructuraWebHandler
from fastapi.templating import Jinja2Templates
from typing import List, Optional

router = APIRouter(tags=["Infraestructura"])
templates = Jinja2Templates(directory="web/templates")

@router.get("/areas")
async def view_areas(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_areas_index(request)

@router.get("/areas/lista")
async def list_areas(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_areas_list(request)

@router.post("/areas/crear")
async def create_area(request: Request, nombre: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_area_crear(request, nombre)

@router.post("/areas/actualizar")
async def update_area(request: Request, id: int = Form(...), nombre: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_area_actualizar(request, id, nombre)

@router.post("/areas/eliminar")
async def delete_area(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_area_eliminar(request, id)

@router.get("/salones")
async def view_salones(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_salones_index(request)

@router.get("/salones/lista")
async def list_salones(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_salones_list(request)

@router.post("/salones/crear")
async def create_salon(request: Request, nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_salon_crear(request, nombre, edad)

@router.post("/salones/actualizar")
async def update_salon(request: Request, id: int = Form(...), nombre: str = Form(...), edad: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_salon_actualizar(request, id, nombre, edad)

@router.post("/salones/eliminar")
async def delete_salon(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_salon_eliminar(request, id)

@router.get("/recepciones")
async def view_recepciones(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_recepciones_index(request)

@router.get("/recepciones/lista")
async def list_recepciones(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_recepciones_list(request)

@router.post("/recepciones/crear")
async def create_recepcion(request: Request, nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_recepcion_crear(request, nombre, fecha)

@router.post("/recepciones/actualizar")
async def update_recepcion(request: Request, id: int = Form(...), nombre: str = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_recepcion_actualizar(request, id, nombre, fecha)

@router.post("/recepciones/eliminar")
async def delete_recepcion(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_recepcion_eliminar(request, id)

# Aulas
@router.get("/aulas")
async def view_aulas(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_aulas_index(request)

@router.get("/aulas/lista")
async def list_aulas(request: Request, fecha: str = Query(None), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_aulas_list(request, fecha)

@router.post("/aulas/crear")
async def create_aula(
    request: Request, id_salon: int = Form(...), id_maestra: Optional[int] = Form(None),
    id_auxiliar: Optional[int] = Form(None), ids_colaboradores: List[int] = Form([]),
    ninos: int = Form(0), ninas: int = Form(0), condicion: str = Form(...),
    fecha: str = Form(...), db: Session = Depends(get_db)
):
    datos = {
        "id_salon": id_salon, "id_maestra": id_maestra, "id_auxiliar": id_auxiliar,
        "ids_colaboradores": ids_colaboradores, "ninos": ninos, "ninas": ninas,
        "condicion": condicion, "fecha": fecha
    }
    return await InfraestructuraWebHandler(db, templates).post_aula_crear(request, datos)

@router.post("/aulas/actualizar")
async def update_aula(
    request: Request, id: int = Form(...), id_salon: int = Form(...), id_maestra: Optional[int] = Form(None),
    id_auxiliar: Optional[int] = Form(None), ids_colaboradores: List[int] = Form([]),
    ninos: int = Form(0), ninas: int = Form(0), condicion: str = Form(...),
    fecha: str = Form(...), db: Session = Depends(get_db)
):
    datos = {"id_salon": id_salon, "id_maestra": id_maestra, "id_auxiliar": id_auxiliar, "ids_colaboradores": ids_colaboradores, "ninos": ninos, "ninas": ninas, "condicion": condicion, "fecha": fecha}
    return await InfraestructuraWebHandler(db, templates).post_aula_actualizar(request, id, datos)

@router.post("/aulas/eliminar")
async def delete_aula(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_aula_eliminar(request, id)

# Enseñanza
@router.get("/ensenanza")
async def view_ensenanza(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_ensenanza_index(request)

@router.get("/ensenanza/lista")
async def list_ensenanza(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_ensenanza_list(request)

@router.post("/ensenanza/crear")
async def create_ensenanza(request: Request, capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_ensenanza_crear(request, capitan, subcapitan, fecha)

@router.post("/ensenanza/actualizar")
async def update_ensenanza(request: Request, id: int = Form(...), capitan: str = Form(...), subcapitan: int = Form(...), fecha: str = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_ensenanza_actualizar(request, id, capitan, subcapitan, fecha)

@router.post("/ensenanza/eliminar")
async def delete_ensenanza(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_ensenanza_eliminar(request, id)

# Logística
@router.get("/logistica")
async def view_logistica(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_logistica_index(request)

@router.get("/logistica/lista")
async def list_logistica(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_logistica_list(request, fecha)

@router.post("/logistica/crear")
async def create_logistica(
    request: Request, fecha: str = Form(...), id_capitan: int = Form(None), id_almacen: int = Form(None),
    id_distribucion: int = Form(None), id_hidratacion: int = Form(None), id_pasillo: int = Form(None),
    id_secretaria: int = Form(None), observaciones: str = Form(None), db: Session = Depends(get_db)
):
    datos = {"fecha": fecha, "id_capitan": id_capitan, "id_almacen": id_almacen, "id_distribucion": id_distribucion, "id_hidratacion": id_hidratacion, "id_pasillo": id_pasillo, "id_secretaria": id_secretaria, "observaciones": observaciones}
    return await InfraestructuraWebHandler(db, templates).post_logistica_crear(request, datos)

@router.post("/logistica/actualizar")
async def update_logistica(
    request: Request, id: int = Form(...), almacen: int = Form(...), capitan: int = Form(...),
    distribucion: int = Form(0), hidratacion: int = Form(0), pasillo: int = Form(0),
    secretaria: int = Form(0), fecha: str = Form(...), db: Session = Depends(get_db)
):
    datos = {"almacen": almacen, "capitan": capitan, "distribucion": distribucion, "hidratacion": hidratacion, "pasillo": pasillo, "secretaria": secretaria, "fecha": fecha}
    return await InfraestructuraWebHandler(db, templates).post_logistica_actualizar(request, id, datos)

@router.post("/logistica/eliminar")
async def delete_logistica(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_logistica_eliminar(request, id)

# Otras Áreas
@router.get("/otras_areas")
async def view_otrasareas(request: Request, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_otrasareas_index(request)

@router.get("/otras_areas/lista")
async def list_otrasareas(request: Request, fecha: str = None, db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).get_otrasareas_list(request, fecha)

@router.post("/otras_areas/crear")
async def create_otrasareas(
    request: Request, alabanza: int = Form(0), protocolo: int = Form(0), semillitas: int = Form(0),
    sonido: int = Form(0), teatro: int = Form(0), tv: int = Form(0), ujier: int = Form(0),
    seguridad: int = Form(0), fecha: str = Form(...), db: Session = Depends(get_db)
):
    datos = {"alabanza": alabanza, "protocolo": protocolo, "semillitas": semillitas, "sonido": sonido, "teatro": teatro, "tv": tv, "ujier": ujier, "seguridad": seguridad, "fecha": fecha}
    return await InfraestructuraWebHandler(db, templates).post_otrasareas_crear(request, datos)

@router.post("/otras_areas/actualizar")
async def update_otrasareas(
    request: Request, id: int = Form(...), alabanza: int = Form(0), protocolo: int = Form(0), semillitas: int = Form(0),
    sonido: int = Form(0), teatro: int = Form(0), tv: int = Form(0), ujier: int = Form(0),
    seguridad: int = Form(0), fecha: str = Form(...), db: Session = Depends(get_db)
):
    datos = {"alabanza": alabanza, "protocolo": protocolo, "semillitas": semillitas, "sonido": sonido, "teatro": teatro, "tv": tv, "ujier": ujier, "seguridad": seguridad, "fecha": fecha}
    return await InfraestructuraWebHandler(db, templates).post_otrasareas_actualizar(request, id, datos)

@router.post("/otras_areas/eliminar")
async def delete_otrasareas(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await InfraestructuraWebHandler(db, templates).post_otrasareas_eliminar(request, id)