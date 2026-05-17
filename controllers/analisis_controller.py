import logging
from sqlalchemy import func
from controllers.base_controller import BaseController
from models.donaciones import Donacion
from models.logistica import Logistica
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AnalisisController(BaseController):
    def __init__(self, session=None):
        super().__init__(session=session)

    def obtener_resumen_donaciones(self, dias=30):
        """Calcula tendencias de donaciones en los últimos N días."""
        db = self.get_db_session()
        try:
            fecha_limite = datetime.utcnow() - timedelta(days=dias)
            
            # Agrupación por fecha
            stats = db.query(
                Donacion.fecha,
                func.count(Donacion.id).label('total_donaciones'),
                func.sum(Donacion.cantidad).label('volumen_total')
            ).filter(
                Donacion.fecha >= fecha_limite,
                Donacion.is_deleted.is_(False)
            ).group_by(Donacion.fecha).order_by(Donacion.fecha).all()

            return [
                {"fecha": s.fecha.isoformat(), "cantidad": s.total_donaciones, "volumen": float(s.volumen_total or 0)}
                for s in stats
            ]
        except Exception as e:
            logger.error(f"Error en resumen de donaciones: {e}")
            return []
        finally:
            if not self.session: db.close()

    def obtener_metricas_operativas(self):
        """Métricas rápidas de logística y cobertura."""
        db = self.get_db_session()
        try:
            total_logistica = db.query(func.count(Logistica.id)).filter(Logistica.is_deleted.is_(False)).scalar()
            
            # Ejemplo: Promedio de servidores por jornada de logística
            # (Suma de campos de puestos / total de registros)
            # Esto asume que los campos en Logistica son 1 o 0
            return {
                "total_jornadas": total_logistica,
                "mensaje": "Métricas listas para visualización"
            }
        except Exception as e:
            logger.error(f"Error en métricas operativas: {e}")
            return {}
        finally:
            if not self.session: db.close()

    def asistente_ai_query(self, query_texto):
        """Placeholder para el Agente Analista con Gemini."""
        # Aquí es donde integrarías el SDK de Google Generative AI
        pass