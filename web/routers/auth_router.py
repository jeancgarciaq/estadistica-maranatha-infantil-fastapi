from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from models.database import get_db
from web.handlers.auth_handler import AuthWebHandler
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(tags=["Autenticación"])
templates = Jinja2Templates(directory="web/templates")
templates.env.globals["prefix"] = "/semi"

@router.get("/")
@router.get("/login")
async def login_view(request: Request, db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.get_login(request)

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.post_login(request, username, password)

@router.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.get_logout(request)

@router.get("/register")
async def register_view(request: Request, db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.get_register(request)

@router.post("/register")
async def register_post(
    request: Request,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    rol_nombre: Optional[str] = Form(None),
    math_answer: Optional[int] = Form(None),
    math_expected: Optional[int] = Form(None),
    website: str = Form(None), # Honeypot
    db: Session = Depends(get_db)
):
    handler = AuthWebHandler(db, templates)
    datos = {"username": username, "password": password, "rol_nombre": rol_nombre, "website": website}
    return await handler.post_register(request, datos, math_answer, math_expected)

@router.get("/forgot-password")
async def forgot_password_view(request: Request, db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.get_forgot_password(request)

@router.post("/forgot-password")
async def forgot_password_post(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.post_forgot_password(request, email)

@router.get("/reset-password/{token}")
async def reset_password_view(request: Request, token: str, db: Session = Depends(get_db)):
    handler = AuthWebHandler(db, templates)
    return await handler.get_reset_password(request, token)

@router.post("/reset-password/{token}")
async def reset_password_post(
    request: Request, token: str, password: str = Form(...),
    confirm_password: str = Form(...), db: Session = Depends(get_db)
):
    handler = AuthWebHandler(db, templates)
    return await handler.post_reset_password(request, token, password, confirm_password)