from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import status, Request

class BaseWebHandler:
    PREFIX = ""

    def __init__(self, templates: Jinja2Templates):
        self.templates = templates

    def render(self, request: Request, template_name: str, context: dict = None):
        """Renderiza un template con el contexto base."""
        full_context = {"request": request}
        if hasattr(request.state, "user"):
            full_context["user"] = request.state.user
        if context:
            full_context.update(context)
        return self.templates.TemplateResponse(request, template_name, full_context)

    def redirect(self, url: str, msg: str = None, type: str = "success", request: Request = None):
        """Crea una redirección absoluta para evitar que Starlette borre /semi."""
        
        # 1. Asegurar que la ruta empiece con /semi (evitar duplicación)
        if not url.startswith(self.PREFIX):
            url = f"{self.PREFIX}{url}" if url.startswith("/") else f"{self.PREFIX}/{url}"
        # Si ya empieza con /semi, usarla tal cual

        # 2. Agregar mensaje flash si existe
        final_path = f"{url}?msg={msg}&type={type}" if msg else url

        # 3. Construir URL Absoluta si tenemos el request
        if request:
            # Reconstruye https://administromicondominio.com/semi/login
            scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
            host = request.headers.get("host", request.url.netloc)
            target_url = f"{scheme}://{host}{final_path}"
        else:
            # Fallback seguro - usar URL relativa en lugar de absoluta hardcodeada
            target_url = final_path

        return RedirectResponse(url=target_url, status_code=status.HTTP_303_SEE_OTHER)