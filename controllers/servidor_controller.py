import logging
from sqlalchemy.orm import selectinload
from controllers.base_controller import BaseController
from models.servidor import Servidor
from models.capitanes import Capitan
from models.coordinadores import Coordinador

logger = logging.getLogger(__name__)

class ServidorController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Servidor, session=session)

    def crear_servidor(self, datos: dict, user_context=None):
        nombre = datos.get('nombre', '').strip()
        try:
            cedula = int(datos.get('cedula')) if datos.get('cedula') else None
        except (ValueError, TypeError):
            return False, "La cédula debe ser un valor numérico."

        correo = datos.get('correo', '').strip() or None

        if not nombre or not cedula:
            return False, "Nombre y Cédula son campos obligatorios."

        def operacion(db):
            if db.query(Servidor).filter(Servidor.cedula == cedula, Servidor.is_deleted.is_(False)).first():
                raise ValueError(f"Ya existe un servidor con la cédula {cedula}.")

            if correo:
                if db.query(Servidor).filter(Servidor.correo == correo, Servidor.is_deleted.is_(False)).first():
                    raise ValueError(f"El correo {correo} ya está registrado.")

            id_capitan = datos.get('id_capitan')
            if not id_capitan and datos.get('capitan'):
                cap_obj = db.query(Capitan).filter(Capitan.nombre == datos['capitan'].strip()).first()
                if cap_obj:
                    id_capitan = cap_obj.id

            nuevo_servidor = Servidor(
                nombre=nombre,
                cedula=cedula,
                correo=correo,
                celular=datos.get('celular'),
                numero_equipo=int(datos.get('numero_equipo')) if datos.get('numero_equipo') else None,
                fecha_nacimiento=datos.get('fecha_nacimiento'),
                id_capitan=id_capitan
            )

            if not nuevo_servidor.fecha_nacimiento:
                try:
                    nuevo_servidor.edad = int(datos.get('edad'))
                except (ValueError, TypeError):
                    raise ValueError("Debe proporcionar la edad o la fecha de nacimiento.")

            db.add(nuevo_servidor)
            logger.info(f"Servidor '{nombre}' creado exitosamente.")

        return self.ejecutar_transaccion(operacion, "Servidor creado exitosamente.", user_context=user_context)

    def actualizar_servidor(self, id, datos: dict, user_context=None):
        if not id or not isinstance(id, int):
            return False, "El ID del servidor es obligatorio y debe ser un número entero."

        def operacion(db):
            servidor = db.query(Servidor).filter(Servidor.id == id, Servidor.is_deleted.is_(False)).first()
            if not servidor:
                raise ValueError("Servidor no encontrado.")

            servidor.nombre = datos.get('nombre', servidor.nombre).strip()
            servidor.celular = datos.get('celular', servidor.celular)
            servidor.correo = datos.get('correo', servidor.correo).strip() or None
            servidor.numero_equipo = int(datos.get('numero_equipo')) if datos.get('numero_equipo') else None
            servidor.fecha_nacimiento = datos.get('fecha_nacimiento', servidor.fecha_nacimiento)
            servidor.id_capitan = datos.get('id_capitan', servidor.id_capitan)

            if not servidor.fecha_nacimiento:
                try:
                    servidor.edad = int(datos.get('edad'))
                except (ValueError, TypeError):
                    raise ValueError("Debe proporcionar la edad o la fecha de nacimiento.")

            db.add(servidor)
            logger.info(f"Servidor '{servidor.nombre}' actualizado.")

        return self.ejecutar_transaccion(operacion, "Servidor actualizado exitosamente.", user_context=user_context)

    def listar_servidores(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).options(
                selectinload(Servidor.capitan).selectinload(Capitan.coordinador).selectinload(Coordinador.area)
            ).all()
        finally:
            if not self.session:
                db.close()

    def eliminar_servidor(self, id, user_context=None):
        if not id or not isinstance(id, int):
            return False, "El ID del servidor es obligatorio."
        def operacion(db):
            servidor = db.query(Servidor).filter(Servidor.id == id, Servidor.is_deleted.is_(False)).first()
            if not servidor:
                raise ValueError("Servidor no encontrado.")
            self.marcar_eliminado(servidor, db)
        return self.ejecutar_transaccion(operacion, "Servidor eliminado exitosamente.", user_context=user_context)
