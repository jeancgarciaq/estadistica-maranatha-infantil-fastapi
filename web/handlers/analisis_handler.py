from sqlalchemy.orm import Session
from controllers.analisis_controller import AnalisisController
from web.handlers.base_handler import BaseWebHandler

class AnalisisWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.controller = AnalisisController(db)

    async def get_analisis_index(self, request):
        """
        Obtiene las estadísticas desde el controlador y renderiza la vista de análisis.
        """
        # Obtener datos para los gráficos y métricas
        donaciones = self.controller.obtener_resumen_donaciones()
        metricas = self.controller.obtener_metricas_operativas()

        return self.render(request, "analisis/analisis.html", {
            "datos_donaciones": donaciones,
            "metricas": metricas
        })