import logging
from sqlalchemy.exc import SQLAlchemyError
from controllers.base_controller import BaseController
from models.servidor import Servidor
from models.areas import Area
from models.capitanes import Capitan

logger = logging.getLogger(__name__)

class ServidorController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Servidor, session=session)

    def crear_servidor(self, datos: dict, user_context=None):
        """
        Crea un nuevo servidor validando duplicados y resolviendo IDs de relaciones.
        """
        # Limpieza y validación básica
        nombre = datos.get('nombre', '').strip()
        try:
            # Forzamos que la cédula sea entero para evitar errores de tipo en SQLite/Postgres
            cedula = int(datos.get('cedula')) if datos.get('cedula') else None
        except (ValueError, TypeError):
            return False, "La cédula debe ser un valor numérico."
            
        correo = datos.get('correo', '').strip() or None
        
        if not nombre or not cedula:
            return False, "Nombre y Cédula son campos obligatorios."

        def operacion(db):
            # 1. Validar Restricciones Únicas (Evita fallos críticos de integridad)
            if db.query(Servidor).filter(Servidor.cedula == cedula, Servidor.is_deleted.is_(False)).first():
                raise ValueError(f"Ya existe un servidor con la cédula {cedula}.")
            
            if correo:
                if db.query(Servidor).filter(Servidor.correo == correo, Servidor.is_deleted.is_(False)).first():
                    raise ValueError(f"El correo {correo} ya está registrado.")

            # 2. Resolución de Relaciones (Mapping de nombres a IDs)
            id_area = datos.get('id_area')
            if not id_area and datos.get('area_servicio'):
                area_obj = db.query(Area).filter(Area.area == datos['area_servicio'].strip()).first()
                if area_obj:
                    id_area = area_obj.id

            id_capitan = datos.get('id_capitan')
            if not id_capitan and datos.get('capitan'):
                cap_obj = db.query(Capitan).filter(Capitan.nombre == datos['capitan'].strip()).first()
                if cap_obj:
                    id_capitan = cap_obj.id

            # 3. Crear instancia del modelo
            nuevo_servidor = Servidor(
                nombre=nombre,
                cedula=cedula,
                correo=correo,
                celular=datos.get('celular'),
                numero_equipo=int(datos.get('numero_equipo')) if datos.get('numero_equipo') else None,
                fecha_nacimiento=datos.get('fecha_nacimiento'),
                id_area=id_area,
                id_capitan=id_capitan
            )
            
            # Si no se envía fecha, la edad es obligatoria (según tu modelo nullable=False)
            if not nuevo_servidor.fecha_nacimiento:
                try:
                    nuevo_servidor.edad = int(datos.get('edad'))
                except (ValueError, TypeError):
                    raise ValueError("Debe proporcionar la edad o la fecha de nacimiento.")

            db.add(nuevo_servidor)
            logger.info(f"Servidor '{nombre}' preparado para guardado local y sincronización.")

        return self.ejecutar_transaccion(operacion, "Servidor creado exitosamente.", user_context=user_context)

    def listar_servidores(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).all()
        finally:
            if not self.session:
                db.close()