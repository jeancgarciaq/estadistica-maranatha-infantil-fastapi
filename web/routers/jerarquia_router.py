from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.jerarquia_handler import JerarquiaWebHandler
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Jerarquía"])
templates = Jinja2Templates(directory="web/templates")

@router.get("/pastores")
async def view_pastores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_pastores_index(request)

@router.get("/pastores/lista")
async def list_pastores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_pastores_list(request)

@router.post("/pastores/crear")
async def create_pastor(request: Request, nombre: str = Form(...), iglesia: str = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_pastor_crear(request, {"nombre": nombre, "iglesia": iglesia})

@router.get("/lideres")
async def view_lideres(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_lideres_index(request)

@router.get("/lideres/lista")
async def list_lideres(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_lideres_list(request)

@router.get("/coordinadores")
async def view_coordinadores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_coordinadores_index(request)

@router.get("/coordinadores/lista")
async def list_coordinadores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_coordinadores_list(request)

@router.get("/capitanes")
async def view_capitanes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_capitanes_index(request)

@router.get("/capitanes/lista")
async def list_capitanes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_capitanes_list(request)

# Rutas de Docentes
@router.get("/docentes")
async def view_docentes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_docentes_index(request)

@router.get("/docentes/lista")
async def list_docentes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_docentes_list(request)

@router.post("/docentes/crear")
async def create_docente(request: Request, nombre: str = Form(...), cedula: int = Form(...), edad: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_docente_crear(request, {"nombre": nombre, "cedula": cedula, "edad": edad})

# Rutas de Auxiliares
@router.get("/auxiliares")
async def view_auxiliares(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_auxiliares_index(request)

@router.get("/auxiliares/lista")
async def list_auxiliares(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_auxiliares_list(request)

@router.post("/auxiliares/crear")
async def create_auxiliar(request: Request, nombre: str = Form(...), cedula: int = Form(...), edad: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_auxiliar_crear(request, {"nombre": nombre, "cedula": cedula, "edad": edad})

# Rutas de Colaboradores
@router.get("/colaboradores")
async def view_colaboradores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_colaboradores_index(request)

@router.get("/colaboradores/lista")
async def list_colaboradores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_colaboradores_list(request)

@router.post("/colaboradores/crear")
async def create_colaborador(request: Request, nombre: str = Form(...), cedula: int = Form(...), edad: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_colaborador_crear(request, {"nombre": nombre, "cedula": cedula, "edad": edad})
