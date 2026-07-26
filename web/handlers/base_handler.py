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
        # Asegurar prefijo /semi
        if not url.startswith(self.PREFIX):
            url = f"{self.PREFIX}{url}" if url.startswith("/") else f"{self.PREFIX}/{url}"

        final_url = f"{url}?msg={msg}&type={type}" if msg else url
        
        # Creamos la respuesta 303 forzando la cabecera Location exacta sin que Starlette la altere
        response = RedirectResponse(url=final_url, status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Location"] = final_url
        return response