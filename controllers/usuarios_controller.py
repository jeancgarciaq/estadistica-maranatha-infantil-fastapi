import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from controllers.base_controller import BaseController
from models.security import (
    ROLE_ROOT,
    Permiso,
    Rol,
    Usuario,
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
            user = (
                db.query(Usuario)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(Usuario.username == username.strip(), Usuario.password == password, Usuario.activo == True)
                .first()
            )
            if not user:
                return False, None, 'Credenciales inválidas o usuario inactivo.'

            db.expunge(user)
            if user.rol:
                db.expunge(user.rol)
                for permiso in user.rol.permisos:
                    db.expunge(permiso)
            return True, user, 'Inicio de sesión exitoso.'
        except SQLAlchemyError as e:
            logger.error('Error autenticando usuario: %s', e)
            return False, None, 'Error interno de autenticación.'
        finally:
            db.close()

    def listar_usuarios(self):
        db = self.get_db_session()
        try:
            return (
                db.query(Usuario)
                .options(joinedload(Usuario.rol))
                .order_by(Usuario.username.asc())
                .all()
            )
        except SQLAlchemyError as e:
            logger.error('Error listando usuarios: %s', e)
            return []
        finally:
            db.close()

    def listar_roles(self):
        db = self.get_db_session()
        try:
            return db.query(Rol).order_by(Rol.nombre.asc()).all()
        except SQLAlchemyError as e:
            logger.error('Error listando roles: %s', e)
            return []
        finally:
            db.close()

    def crear_usuario(self, username, password, rol_nombre):
        if not username or not password or not rol_nombre:
            return False, 'Usuario, contraseña y rol son obligatorios.'

        db = self.get_db_session()
        try:
            existe = db.query(Usuario).filter(Usuario.username == username.strip()).first()
            if existe:
                return False, 'Ya existe un usuario con ese nombre.'

            rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
            if not rol:
                return False, 'Rol inválido.'

            db.add(Usuario(username=username.strip(), password=password, rol_id=rol.id, activo=True))
            db.commit()
            return True, 'Usuario creado exitosamente.'
        except SQLAlchemyError as e:
            db.rollback()
            logger.error('Error creando usuario: %s', e)
            return False, 'No se pudo crear el usuario.'
        finally:
            db.close()

    def actualizar_usuario(self, user_id, password=None, rol_nombre=None, activo=None):
        if not user_id:
            return False, 'Debe indicar el usuario a actualizar.'

        db = self.get_db_session()
        try:
            usuario = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
            if not usuario:
                return False, 'Usuario no encontrado.'

            if usuario.username == 'root' and activo is False:
                return False, 'El usuario root no puede desactivarse.'

            if password is not None and password.strip() != '':
                usuario.password = password.strip()

            if rol_nombre:
                rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
                if not rol:
                    return False, 'Rol inválido.'
                if usuario.username == 'root' and rol.nombre != ROLE_ROOT:
                    return False, 'El usuario root debe mantener el rol root.'
                usuario.rol_id = rol.id

            if activo is not None:
                usuario.activo = bool(activo)

            db.commit()
            return True, 'Usuario actualizado exitosamente.'
        except SQLAlchemyError as e:
            db.rollback()
            logger.error('Error actualizando usuario: %s', e)
            return False, 'No se pudo actualizar el usuario.'
        finally:
            db.close()

    def obtener_usuario(self, user_id):
        db = self.get_db_session()
        try:
            return (
                db.query(Usuario)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(Usuario.id == int(user_id))
                .first()
            )
        except SQLAlchemyError as e:
            logger.error('Error obteniendo usuario: %s', e)
            return None
        finally:
            db.close()

    @staticmethod
    def usuario_tiene_permiso(usuario, permiso_codigo):
        if not usuario or not getattr(usuario, 'rol', None):
            return False

        if usuario.rol.nombre == ROLE_ROOT:
            return True

        permisos = {perm.codigo for perm in (usuario.rol.permisos or [])}
        return permiso_codigo in permisos or '*' in permisos
