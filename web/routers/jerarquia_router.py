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

@router.post("/pastores/actualizar")
async def update_pastor(request: Request, id: int = Form(...), nombre: str = Form(...), iglesia: str = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_pastor_actualizar(request, id, {"nombre": nombre, "iglesia": iglesia})

@router.post("/pastores/eliminar")
async def delete_pastor(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_pastor_eliminar(request, id)

@router.get("/lideres")
async def view_lideres(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_lideres_index(request)

@router.get("/lideres/lista")
async def list_lideres(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_lideres_list(request)

@router.post("/lideres/crear")
async def create_lider(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_pastor: str = Form(None),
    db: Session = Depends(get_db)
):
    id_pastor_val = int(id_pastor) if id_pastor and id_pastor.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_pastor": id_pastor_val
    }
    return await JerarquiaWebHandler(db, templates).post_lider_crear(request, datos)

@router.post("/lideres/actualizar")
async def update_lider(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_pastor: str = Form(None),
    db: Session = Depends(get_db)
):
    id_pastor_val = int(id_pastor) if id_pastor and id_pastor.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_pastor": id_pastor_val
    }
    return await JerarquiaWebHandler(db, templates).post_lider_actualizar(request, id, datos)

@router.post("/lideres/eliminar")
async def delete_lider(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_lider_eliminar(request, id)

@router.get("/coordinadores")
async def view_coordinadores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_coordinadores_index(request)

@router.get("/coordinadores/lista")
async def list_coordinadores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_coordinadores_list(request)

@router.post("/coordinadores/crear")
async def create_coordinador(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_lider: str = Form(None),
    id_area: str = Form(None),
    db: Session = Depends(get_db)
):
    id_lider_val = int(id_lider) if id_lider and id_lider.strip() else None
    id_area_val = int(id_area) if id_area and id_area.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_lider": id_lider_val,
        "id_area": id_area_val
    }
    return await JerarquiaWebHandler(db, templates).post_coordinador_crear(request, datos)

@router.post("/coordinadores/actualizar")
async def update_coordinador(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_lider: str = Form(None),
    id_area: str = Form(None),
    db: Session = Depends(get_db)
):
    id_lider_val = int(id_lider) if id_lider and id_lider.strip() else None
    id_area_val = int(id_area) if id_area and id_area.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_lider": id_lider_val,
        "id_area": id_area_val
    }
    return await JerarquiaWebHandler(db, templates).post_coordinador_actualizar(request, id, datos)

@router.post("/coordinadores/eliminar")
async def delete_coordinador(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_coordinador_eliminar(request, id)



@router.get("/capitanes")
async def view_capitanes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_capitanes_index(request)

@router.get("/capitanes/lista")
async def list_capitanes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_capitanes_list(request)

@router.post("/capitanes/crear")
async def create_capitan(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_coordinador: str = Form(None),
    db: Session = Depends(get_db)
):
    id_coordinador_val = int(id_coordinador) if id_coordinador and id_coordinador.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_coordinador": id_coordinador_val
    }
    return await JerarquiaWebHandler(db, templates).post_capitan_crear(request, datos)

@router.post("/capitanes/actualizar")
async def update_capitan(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_coordinador: str = Form(None),
    db: Session = Depends(get_db)
):
    id_coordinador_val = int(id_coordinador) if id_coordinador and id_coordinador.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_coordinador": id_coordinador_val
    }
    return await JerarquiaWebHandler(db, templates).post_capitan_actualizar(request, id, datos)

@router.post("/capitanes/eliminar")
async def delete_capitan(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_capitan_eliminar(request, id)

# Rutas de Docentes
@router.get("/docentes")
async def view_docentes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_docentes_index(request)

@router.get("/docentes/lista")
async def list_docentes(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_docentes_list(request)

@router.post("/docentes/crear")
async def create_docente(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_docente_crear(request, datos)

@router.post("/docentes/actualizar")
async def update_docente(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_docente_actualizar(request, id, datos)

@router.post("/docentes/eliminar")
async def delete_docente(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_docente_eliminar(request, id)

# Rutas de Auxiliares
@router.get("/auxiliares")
async def view_auxiliares(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_auxiliares_index(request)

@router.get("/auxiliares/lista")
async def list_auxiliares(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_auxiliares_list(request)

@router.post("/auxiliares/crear")
async def create_auxiliar(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_auxiliar_crear(request, datos)

@router.post("/auxiliares/actualizar")
async def update_auxiliar(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_auxiliar_actualizar(request, id, datos)

@router.post("/auxiliares/eliminar")
async def delete_auxiliar(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_auxiliar_eliminar(request, id)

# Rutas de Colaboradores
@router.get("/colaboradores")
async def view_colaboradores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_colaboradores_index(request)

@router.get("/colaboradores/lista")
async def list_colaboradores(request: Request, db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).get_colaboradores_list(request)

@router.post("/colaboradores/crear")
async def create_colaborador(
    request: Request,
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_colaborador_crear(request, datos)

@router.post("/colaboradores/actualizar")
async def update_colaborador(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    cedula: int = Form(...),
    edad: int = Form(...),
    fecha_nacimiento: str = Form(None),
    celular: str = Form(None),
    correo: str = Form(None),
    id_capitan: str = Form(None),
    numero_equipo: str = Form(None),
    db: Session = Depends(get_db)
):
    id_capitan_val = int(id_capitan) if id_capitan and id_capitan.strip() else None
    numero_equipo_val = int(numero_equipo) if numero_equipo and numero_equipo.strip() else None
    datos = {
        "nombre": nombre,
        "cedula": cedula,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento if fecha_nacimiento and fecha_nacimiento.strip() else None,
        "celular": celular if celular and celular.strip() else None,
        "correo": correo if correo and correo.strip() else None,
        "id_capitan": id_capitan_val,
        "numero_equipo": numero_equipo_val
    }
    return await JerarquiaWebHandler(db, templates).post_colaborador_actualizar(request, id, datos)

@router.post("/colaboradores/eliminar")
async def delete_colaborador(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    return await JerarquiaWebHandler(db, templates).post_colaborador_eliminar(request, id)
