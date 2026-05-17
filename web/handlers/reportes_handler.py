import os
import logging
from fastapi.responses import FileResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.reporte_estadistico import ReporteEstadisticoService
from web.handlers.base_handler import BaseWebHandler

logger = logging.getLogger(__name__)

class ReportesWebHandler(BaseWebHandler):
    def __init__(self, db: Session, templates):
        super().__init__(templates)
        self.db = db
        self.servicio = ReporteEstadisticoService(db)

    async def get_reportes_index(self, request, fecha: str = None):
        resumen_texto = "Seleccione una fecha y genere el resumen."
        if fecha:
            try:
                resumen_data = self.servicio.obtener_resumen(fecha)
                resumen_texto = self.servicio.formatear_vista_previa(resumen_data)
            except Exception as e:
                logger.error(f"Error al generar resumen para la web: {e}")
                resumen_texto = f"Error al generar resumen: {e}"

        return self.render(request, "reportes/index.html", {
            "fecha_filtro": fecha,
            "resumen_texto": resumen_texto
        })

    async def post_generar_pdf(self, request, fecha: str):
        if not fecha:
            raise HTTPException(status_code=400, detail="Debe seleccionar una fecha para generar el PDF.")
        
        try:
            resumen = self.servicio.obtener_resumen(fecha)
            graficos = self.servicio.generar_graficos(resumen)
            pdf_file_path = self.servicio.generar_pdf(resumen, graficos)
            
            return FileResponse(
                path=pdf_file_path,
                media_type="application/pdf",
                filename=os.path.basename(pdf_file_path)
            )
        except ModuleNotFoundError as e:
            logger.error(f"Error: {e}. Reportlab no está instalado.")
            raise HTTPException(status_code=500, detail=f"Error en el servidor: {e}. Asegúrese de que reportlab esté instalado.")
        except Exception as e:
            logger.error(f"Error al generar PDF: {e}")
            raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {e}")