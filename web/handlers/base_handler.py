from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import status

class BaseWebHandler:
    PREFIX = "/semi"

    def __init__(self, templates: Jinja2Templates):
        self.templates = templates

    def render(self, request, template_name: str, context: dict = None):
        """Renderiza un template con el contexto base (usuario, etc)."""
        full_context = {"request": request}
        if hasattr(request.state, "user"):
            full_context["user"] = request.state.user
        if context:
            full_context.update(context)
        return self.templates.TemplateResponse(request, template_name, full_context)

    def redirect(self, url: str, msg: str = None, type: str = "success"):
        """Crea una redirección con mensaje flash opcional asegurando el prefijo."""
        # 1. Si la URL empieza con '/' y NO empieza ya con '/semi', le añadimos el prefijo
        if url.startswith("/") and not url.startswith(self.PREFIX):
            url = f"{self.PREFIX}{url}"
        
        # 2. Si la URL viene como "" o "/", la enviamos a la raíz del prefijo "/semi"
        elif url == "":
            url = self.PREFIX

        # 3. Construcción de URL final con mensaje flash
        final_url = f"{url}?msg={msg}&type={type}" if msg else url
        return RedirectResponse(url=final_url, status_code=status.HTTP_303_SEE_OTHER)