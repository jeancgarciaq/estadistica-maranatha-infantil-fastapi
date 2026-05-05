import logging
import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from controllers.base_controller import BaseController
from models.security import (
    ROLE_ROOT, ROLE_LIMITS,
    Permiso, 
    Rol,
    Usuario,
    pwd_context # Import pwd_context for password hashing
)
 
logger = logging.getLogger(__name__)

class UsuariosController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Usuario, session=session)

    def autenticar(self, username, password):
        if not username or not password:
            return False, None, 'Debe indicar usuario y contraseña.'

        db = self.get_db_session()
        try:
            # Buscamos el usuario por nombre para validar password y estado de forma separada en logs internos
            user_record = (
                db.query(Usuario)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(Usuario.username == username.strip(), Usuario.is_deleted.is_(False))
                .first()
            )

            if not user_record:
                logger.warning("Fallo login local: Usuario '%s' no encontrado o eliminado.", username)
                return False, None, 'Credenciales inválidas o usuario inactivo.'

            if not user_record.verify_password(password) or not user_record.activo:
                logger.warning("Fallo login local para '%s': Contraseña incorrecta o usuario inactivo (activo=%s).", username, user_record.activo)
                return False, None, 'Credenciales inválidas o usuario inactivo.'

            return True, user_record, 'Inicio de sesión exitoso.'
        except SQLAlchemyError as e:
            logger.error('Error autenticando usuario: %s', e)
            return False, None, 'Error interno de autenticación.'
        finally:
            if not self.session:
                db.close()

    def listar_usuarios(self):
        db = self.get_db_session()
        try:
            return (
                self.query_activa(db)
                .options(joinedload(Usuario.rol))
                .order_by(Usuario.username.asc())
                .all()
            )
        finally:
            if not self.session:
                db.close()

    def listar_roles(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Rol.nombre.asc()).all()
        except SQLAlchemyError as e:
            logger.error('Error listando roles: %s', e)
            return []
        finally:
            if not self.session:
                db.close()

    def registrar_usuario(self, datos: dict, user_context=None):
        """
        Registro de usuario con validación de límites de roles y anti-spam.
        :param datos: dict con username, password, rol_nombre y 'honeypot'.
        """
        # Anti-Bot: Honeypot (campo invisible que los humanos no llenan)
        if datos.get('website'): 
            return False, 'Petición rechazada por sospecha de bot.'

        username = datos.get('username', '').strip()
        rol_nombre = datos.get('rol_nombre')

        if not username or not datos.get('password') or not rol_nombre:
            return False, 'Todos los campos son obligatorios.'

        def operacion(db):
            # 1. Validar si ya existe
            existe = self.query_activa(db).filter(Usuario.username == username).first()
            if existe:
                raise ValueError('Ya existe un usuario con ese nombre.')

            # 2. Validar Rol y Límites
            rol = self.query_activa(db).filter(Rol.nombre == rol_nombre).first()
            if not rol:
                raise ValueError('Rol inválido.')
            
            conteo_actual = db.query(Usuario).filter(Usuario.rol_id == rol.id, Usuario.is_deleted.is_(False)).count()
            limite = ROLE_LIMITS.get(rol_nombre, 0)
            
            if limite > 0 and conteo_actual >= limite: # Solo aplicar límite si es > 0
                raise ValueError(f'Se ha alcanzado el límite máximo de usuarios para el rol: {rol_nombre} ({limite}).')

            nuevo_usuario = Usuario()
            setattr(nuevo_usuario, 'username', username)
            setattr(nuevo_usuario, 'password', Usuario.hash_password(datos['password']))
            setattr(nuevo_usuario, 'rol_id', rol.id)
            setattr(nuevo_usuario, 'activo', True)

            db.add(nuevo_usuario)
            db.flush()  # Necesario para obtener el ID antes de encolar
            self.registrar_evento_sync(db, 'usuarios', nuevo_usuario, 'upsert')

        return self.ejecutar_transaccion(operacion, 'Usuario creado exitosamente.', user_context=user_context)

    def actualizar_usuario(self, user_id, password=None, rol_nombre=None, activo=None, user_context=None):
        if not user_id:
            return False, 'Debe indicar el usuario a actualizar.'

        def operacion(db):
            usuario = self.query_activa(db).filter(Usuario.id == int(user_id)).first()
            if not usuario:
                raise ValueError('Usuario no encontrado.')

            if getattr(usuario, 'username', None) == 'root' and activo is False:
                raise ValueError('El usuario root no puede desactivarse.')

            if password and password.strip():
                setattr(usuario, 'password', Usuario.hash_password(password))

            if rol_nombre:
                rol = self.query_activa(db).filter(Rol.nombre == rol_nombre).first()
                if not rol:
                    raise ValueError('Rol inválido.')
                if getattr(usuario, 'username', None) == 'root' and getattr(rol, 'nombre', None) != ROLE_ROOT:
                    raise ValueError('El usuario root debe mantener el rol root.')
                setattr(usuario, 'rol_id', rol.id)

            if activo is not None:
                setattr(usuario, 'activo', bool(activo))

            self.registrar_evento_sync(db, 'usuarios', usuario, 'upsert')
            logger.info("Usuario actualizado localmente y encolado para sync: ID %s", user_id)

        return self.ejecutar_transaccion(operacion, 'Usuario actualizado exitosamente.', user_context=user_context)

    def obtener_usuario(self, user_id):
        db = self.get_db_session()
        try:
            return (
                self.query_activa(db)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(Usuario.id == int(user_id))
                .first()
            )
        except SQLAlchemyError as e:
            logger.error('Error obteniendo usuario: %s', e)
            return None
        finally:
            if not self.session:
                db.close()

    @staticmethod
    def usuario_tiene_permiso(usuario, permiso_codigo):
        if not usuario or not getattr(usuario, 'rol', None):
            return False

        if usuario.rol.nombre == ROLE_ROOT:
            return True

        permisos = {perm.codigo for perm in (usuario.rol.permisos or [])}
        return permiso_codigo in permisos or '*' in permisos
