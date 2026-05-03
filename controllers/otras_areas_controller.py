from controllers.base_controller import BaseController
from models.otras_areas import OtrasAreas
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OtrasAreasController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=OtrasAreas, session=session)
        logger.info("OtrasAreasController inicializado.")

    def crear_otrasareas(self, datos, user_context=None):
        if not datos.get('fecha'):
            return False, "La fecha es obligatoria."

        fecha_obj = self.validar_y_convertir_fecha(datos['fecha'])
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            reg = OtrasAreas(
                alabanza=int(datos.get('alabanza', 0)),
                protocolo=int(datos.get('protocolo', 0)),
                semillitas=int(datos.get('semillitas', 0)),
                sonido=int(datos.get('sonido', 0)),
                teatro=int(datos.get('teatro', 0)),
                tv=int(datos.get('tv', 0)),
                ujier=int(datos.get('ujier', 0)),
                seguridad=int(datos.get('seguridad', 0)),
                fecha=fecha_obj
            )
            db.add(reg)
            db.flush()
            self.registrar_evento_sync(db, 'otras_areas', reg, 'upsert')
            logger.info(f"Registro de Otras Áreas creado para fecha {datos['fecha']}")

        return self.ejecutar_transaccion(operacion, "Registro creado exitosamente.", user_context=user_context)

    def actualizar_otrasareas(self, id, datos, user_context=None):
        if not id or not datos.get('fecha'):
            return False, "ID y fecha son obligatorios."

        fecha_obj = self.validar_y_convertir_fecha(datos['fecha'])
        if not fecha_obj:
            return False, "Formato de fecha incorrecto."

        def operacion(db):
            reg = self.query_activa(db).filter(OtrasAreas.id == id).first()
            if not reg:
                raise ValueError("Registro no encontrado.")
            
            reg.alabanza = int(datos.get('alabanza', 0))
            reg.protocolo = int(datos.get('protocolo', 0))
            reg.semillitas = int(datos.get('semillitas', 0))
            reg.sonido = int(datos.get('sonido', 0))
            reg.teatro = int(datos.get('teatro', 0))
            reg.tv = int(datos.get('tv', 0))
            reg.ujier = int(datos.get('ujier', 0))
            reg.seguridad = int(datos.get('seguridad', 0))
            reg.fecha = fecha_obj
            
            self.registrar_evento_sync(db, 'otras_areas', reg, 'upsert')
            logger.info(f"Registro Otras Áreas actualizado: ID {id}")

        return self.ejecutar_transaccion(operacion, "Registro actualizado exitosamente.", user_context=user_context)
                
    def eliminar_otrasareas(self, id, user_context=None):
        if not id:
            return False, "El ID es obligatorio."

        def operacion(db):
            reg = self.query_activa(db).filter(OtrasAreas.id == id).first()
            if not reg:
                raise ValueError("Registro no encontrado.")
            
            self.marcar_eliminado(reg, db)
            self.registrar_evento_sync(db, 'otras_areas', reg, 'delete')
            logger.info(f"Registro Otras Áreas eliminado: ID {id}")

        return self.ejecutar_transaccion(operacion, "Registro eliminado exitosamente.", user_context=user_context)

    def listar_otrasareas(self, fecha=None):
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if fecha:
                fecha_obj = self.validar_y_convertir_fecha(fecha)
                if fecha_obj:
                    query = query.filter(OtrasAreas.fecha == fecha_obj)
            return query.order_by(OtrasAreas.fecha.desc(), OtrasAreas.id.desc()).all()
        finally:
            if not self.session:
                db.close()