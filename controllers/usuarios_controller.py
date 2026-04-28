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
from utils.firebase_auth import FirebaseAuthService

logger = logging.getLogger(__name__)


class UsuariosController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Usuario, session=session)
        self.firebase_auth = FirebaseAuthService()

    def autenticar(self, username, password):
        if not username or not password:
            return False, None, 'Debe indicar usuario y contraseña.'

        if self.firebase_auth.is_configured():
            try:
                auth_session = self.firebase_auth.sign_in(username, password)
                role_assignment = self.firebase_auth.fetch_role_assignment(auth_session)
                if not role_assignment.get('active', True):
                    return False, None, 'Usuario desactivado para acceso en la aplicación.'

                runtime_user = self.firebase_auth.build_runtime_user(auth_session, role_assignment)
                return True, runtime_user, 'Inicio de sesión exitoso con Firebase.'
            except Exception as exc:
                logger.warning('Autenticación Firebase falló, usando autenticación local: %s', exc)

        db = self.get_db_session()
        try:
            # Buscamos el usuario por nombre para validar password y estado de forma separada en logs internos
            user_record = (
                db.query(Usuario)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(
                    Usuario.username == username.strip(),
                    Usuario.is_deleted.is_(False),
                )
                .first()
            )

            if not user_record:
                logger.warning("Fallo login local: Usuario '%s' no encontrado o eliminado.", username)
                return False, None, 'Credenciales inválidas o usuario inactivo.'
            
            if user_record.password != password or not user_record.activo:
                logger.warning("Fallo login local para '%s': Contraseña incorrecta o usuario inactivo (activo=%s).", username, user_record.activo)
                return False, None, 'Credenciales inválidas o usuario inactivo.'

            user = user_record
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

    def obtener_token_firebase(self, usuario):
        if not usuario:
            return None

        auth_session = getattr(usuario, 'firebase_session', None)
        if not auth_session:
            return None

        try:
            return self.firebase_auth.get_valid_id_token(auth_session)
        except Exception as exc:
            logger.error('No se pudo refrescar token Firebase: %s', exc)
            return None

    def listar_usuarios(self):
        db = self.get_db_session()
        try:
            return (
                db.query(Usuario)
                .options(joinedload(Usuario.rol))
                .filter(Usuario.is_deleted.is_(False))
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
            return db.query(Rol).filter(Rol.is_deleted.is_(False)).order_by(Rol.nombre.asc()).all()
        except SQLAlchemyError as e:
            logger.error('Error listando roles: %s', e)
            return []
        finally:
            db.close()

    def crear_usuario(self, username, password, rol_nombre):
        if not username or not password or not rol_nombre:
            return False, 'Usuario, contraseña y rol son obligatorios.'

        def operacion(db):
            existe = db.query(Usuario).filter(Usuario.username == username.strip(), Usuario.is_deleted.is_(False)).first()
            if existe:
                raise ValueError('Ya existe un usuario con ese nombre.')

            rol = db.query(Rol).filter(Rol.nombre == rol_nombre, Rol.is_deleted.is_(False)).first()
            if not rol:
                raise ValueError('Rol inválido.')

            nuevo_usuario = Usuario()
            setattr(nuevo_usuario, 'username', username.strip())
            setattr(nuevo_usuario, 'password', password)
            setattr(nuevo_usuario, 'rol_id', rol.id)
            setattr(nuevo_usuario, 'activo', True)

            db.add(nuevo_usuario)
            db.flush()  # Necesario para obtener el ID antes de encolar
            self.registrar_evento_sync(db, 'usuarios', nuevo_usuario, 'upsert')
            logger.info("Usuario creado localmente y encolado para sync.")

        return self.ejecutar_transaccion(operacion, 'Usuario creado exitosamente.')

    def actualizar_usuario(self, user_id, password=None, rol_nombre=None, activo=None):
        if not user_id:
            return False, 'Debe indicar el usuario a actualizar.'

        def operacion(db):
            usuario = db.query(Usuario).filter(Usuario.id == int(user_id), Usuario.is_deleted.is_(False)).first()
            if not usuario:
                raise ValueError('Usuario no encontrado.')

            if getattr(usuario, 'username', None) == 'root' and activo is False:
                raise ValueError('El usuario root no puede desactivarse.')

            if password and password.strip():
                setattr(usuario, 'password', password)

            if rol_nombre:
                rol = db.query(Rol).filter(Rol.nombre == rol_nombre, Rol.is_deleted.is_(False)).first()
                if not rol:
                    raise ValueError('Rol inválido.')
                if getattr(usuario, 'username', None) == 'root' and getattr(rol, 'nombre', None) != ROLE_ROOT:
                    raise ValueError('El usuario root debe mantener el rol root.')
                setattr(usuario, 'rol_id', rol.id)

            if activo is not None:
                setattr(usuario, 'activo', bool(activo))

            self.registrar_evento_sync(db, 'usuarios', usuario, 'upsert')
            logger.info("Usuario actualizado localmente y encolado para sync: ID %s", user_id)

        return self.ejecutar_transaccion(operacion, 'Usuario actualizado exitosamente.')

    def obtener_usuario(self, user_id):
        db = self.get_db_session()
        try:
            return (
                db.query(Usuario)
                .options(joinedload(Usuario.rol).joinedload(Rol.permisos))
                .filter(Usuario.id == int(user_id), Usuario.is_deleted.is_(False))
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
