from web.handlers.base_handler import BaseWebHandler

class AyudaWebHandler(BaseWebHandler):
    def __init__(self, templates):
        super().__init__(templates)

    async def get_ayuda_index(self, request):
        return self.render(request, "ayudas/index.html")