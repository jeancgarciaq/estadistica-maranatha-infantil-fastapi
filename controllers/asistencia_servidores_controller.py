from models.asistencia_servidores import AsistenciaServidor
from controllers.base_controller import BaseController
from datetime import date

class AsistenciaServidoresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=AsistenciaServidor, session=session)

    def registrar_asistencia(self, db, id_persona, fecha, rol, categoria, referencia_id):
        """
        Registra la asistencia individual de una persona.
        Este método se llama usualmente dentro de una transacción existente.
        """
        asistencia = AsistenciaServidor(
            id_persona=id_persona,
            fecha=fecha,
            rol=rol,
            categoria_contexto=categoria,
            referencia_id=referencia_id
        )
        db.add(asistencia)
        return asistencia

    def limpiar_asistencias_referencia(self, db, categoria, referencia_id):
        """Elimina asistencias previas para evitar duplicados al editar."""
        asistencias = db.query(AsistenciaServidor).filter(
            AsistenciaServidor.categoria_contexto == categoria,
            AsistenciaServidor.referencia_id == referencia_id
        ).all()
        for a in asistencias:
            db.delete(a)

    def obtener_asistencia_por_fecha(self, fecha):
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(AsistenciaServidor.fecha == fecha).all()
        finally:
            if not self.session:
                db.close()