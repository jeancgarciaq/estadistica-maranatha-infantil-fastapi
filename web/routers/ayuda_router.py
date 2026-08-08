from fastapi import APIRouter, Request
from web.handlers.ayuda_handler import AyudaWebHandler
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/ayuda", tags=["Ayuda"])
templates = Jinja2Templates(directory="web/templates")
templates.env.globals["prefix"] = ""

@router.get("/")
async def view_ayuda(request: Request):
    handler = AyudaWebHandler(templates)
    return await handler.get_ayuda_index(request)