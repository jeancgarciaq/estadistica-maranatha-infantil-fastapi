import logging
from models.otras_areas import OtrasAreas
from controllers.base_controller import BaseController
from sqlalchemy.exc import SQLAlchemyError
# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OtrasAreasController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=OtrasAreas, session=session)
        logger.info("OtrasAreasController inicializado.")

    def crear_otrasareas(self, alabanza, protocolo, semillitas, sonido, teatro, tv, ujier, seguridad, fecha, user_context=None):
        """
        Crea un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if not fecha_dt:
            return False, "Formato de fecha incorrecto o fecha faltante. Debe ser YYYY-MM-DD."

        def operacion(db):
            otrasareas = OtrasAreas(
                alabanza=alabanza,
                protocolo=protocolo,
                semillitas=semillitas,
                sonido=sonido,
                teatro=teatro,
                tv=tv,
                ujier=ujier,
                seguridad=seguridad,
                fecha=fecha_dt
            )
            db.add(otrasareas)
            db.flush()
            self.registrar_evento_sync(db, 'otras_areas', otrasareas, 'upsert')
            logger.info("Otras áreas creadas.")

        return self.ejecutar_transaccion(operacion, "Otras áreas creadas exitosamente.", user_context=user_context)

    def actualizar_otrasareas(self, id, alabanza, protocolo, semillitas, sonido, teatro, tv, ujier, seguridad, fecha, user_context=None):
        """
        Actualiza un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        fecha_dt = self.validar_y_convertir_fecha(fecha)
        if not fecha_dt:
            return False, "Formato de fecha incorrecto o fecha faltante. Debe ser YYYY-MM-DD."

        def operacion(db):
            otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id, OtrasAreas.is_deleted.is_(False)).first()
            if not otrasareas:
                raise ValueError("Otras áreas no encontradas.")
            
            otrasareas.alabanza = alabanza
            otrasareas.protocolo = protocolo
            otrasareas.semillitas = semillitas
            otrasareas.sonido = sonido
            otrasareas.teatro = teatro
            otrasareas.tv = tv
            otrasareas.ujier = ujier
            otrasareas.seguridad = seguridad
            otrasareas.fecha = fecha_dt
            
            self.registrar_evento_sync(db, 'otras_areas', otrasareas, 'upsert')
            logger.info(f"Otras áreas actualizadas: ID {id}")

        return self.ejecutar_transaccion(operacion, "Otras áreas actualizadas exitosamente.", user_context=user_context)

    def eliminar_otrasareas(self, id, user_context=None):
        """
        Elimina un registro de otras áreas.
        :return: (Exito, Mensaje)
        """
        def operacion(db):
            otrasareas = db.query(OtrasAreas).filter(OtrasAreas.id == id, OtrasAreas.is_deleted.is_(False)).first()
            if not otrasareas:
                raise ValueError("Otras áreas no encontradas.")
            
            self.marcar_eliminado(otrasareas, db)
            self.registrar_evento_sync(db, 'otras_areas', otrasareas, 'delete')
            logger.info(f"Otras áreas eliminadas: ID {id}")

        return self.ejecutar_transaccion(operacion, "Otras áreas eliminadas exitosamente.", user_context=user_context)

    def listar_otrasareas(self, fecha=None):
        """
        Lista los registros de otras áreas, opcionalmente filtrados por fecha.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(OtrasAreas.fecha == fecha_dt)

            otrasareas = query.order_by(OtrasAreas.fecha.desc(), OtrasAreas.id.desc()).all()
            logger.info(f"{len(otrasareas)} registros de otras áreas obtenidos.")
            return otrasareas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar otras áreas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_otrasareas(self, id):
        """
        Obtiene un registro de otras áreas por ID.
        :return: Objeto OtrasAreas o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(OtrasAreas.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener otras áreas: {e}")
            return None
        finally:
            if not self.session:
                db.close()