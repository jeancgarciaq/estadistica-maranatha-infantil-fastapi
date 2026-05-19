import logging
import os
import uuid
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
 
logger = logging.getLogger(__name__) # Moved this line to avoid re-declaration

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
            return db.query(Rol).order_by(Rol.nombre.asc()).all()
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
            rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
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
                rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
                if not rol:
                    raise ValueError('Rol inválido.')
                if getattr(usuario, 'username', None) == 'root' and getattr(rol, 'nombre', None) != ROLE_ROOT:
                    raise ValueError('El usuario root debe mantener el rol root.')
                setattr(usuario, 'rol_id', rol.id)

            if activo is not None:
                setattr(usuario, 'activo', bool(activo))

            logger.info("Usuario actualizado localmente: ID %s", user_id)

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

    def solicitar_restablecimiento_contrasena(self, email_o_username, request=None):
        """
        Genera un token de restablecimiento de contraseña y lo guarda en la base de datos.
        Luego, envía un correo electrónico con el enlace.
        """
        db = self.get_db_session()
        try:
            usuario = db.query(Usuario).filter(
                (Usuario.username == email_o_username) | (Usuario.username == email_o_username.split('@')[0])
            ).first()

            if not usuario:
                logger.warning(f"Intento de restablecimiento de contraseña para usuario no encontrado: {email_o_username}")
                # Por seguridad devolvemos True para no revelar si el correo existe
                return True, "Si tu cuenta existe, recibirás un correo electrónico con instrucciones."

            token = str(uuid.uuid4())
            expiracion = datetime.now() + timedelta(hours=1)

            usuario.reset_token = token
            usuario.reset_token_expiry = expiracion
            db.commit()

            # Cargamos variables y limpiamos espacios en la contraseña
            smtp_server = os.getenv("SMTP_SERVER", "").strip()
            smtp_port_raw = os.getenv("SMTP_PORT", "465")
            # Intentamos obtener el correo desde múltiples variantes de nombres comunes
            smtp_email = (os.getenv("SMTP_EMAIL") or os.getenv("SMTP_USER") or os.getenv("SMTP_USERNAME") or "").strip()
            smtp_password = os.getenv("SMTP_PASSWORD", "").replace(" ", "")

            smtp_port = int(smtp_port_raw) if smtp_port_raw.isdigit() else 465

            if not all([smtp_server, smtp_email, smtp_password]):
                missing = []
                if not smtp_server: missing.append("SMTP_SERVER")
                if not smtp_email: missing.append("SMTP_EMAIL/SMTP_USER")
                if not smtp_password: missing.append("SMTP_PASSWORD")
                logger.error(f"Configuración SMTP incompleta en .env. Faltan: {', '.join(missing)}")
                return False, "Error interno: Configuración de correo incompleta."

            # 2. Construir enlace usando la URL pública actual o una base configurable
            base_url = None
            if request is not None:
                base_url = str(request.base_url)

            if not base_url:
                base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

            reset_link = f"{base_url.rstrip('/')}/reset-password/{token}"
            
            mensaje_texto = (
                f"Hola {usuario.username},\n\n"
                f"Has solicitado restablecer tu contraseña. Haz clic aquí para continuar:\n{reset_link}\n\n"
                "Este enlace es válido por 1 hora.\n\n"
                "Si no solicitaste esto, ignora este correo."
            )
            
            msg = MIMEText(mensaje_texto)
            msg['Subject'] = "Restablecimiento de Contraseña - EMI"
            msg['From'] = smtp_email

            # Si el username es 'root', enviamos el correo a la cuenta configurada para pruebas
            destinatario = usuario.username if "@" in usuario.username else smtp_email
            msg['To'] = destinatario

            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_email, smtp_password)
                server.send_message(msg)

            logger.info(f"Correo de recuperación enviado a {destinatario}")
            return True, "Si tu cuenta existe, recibirás un correo electrónico con instrucciones."
        except Exception as e:
            if db: db.rollback()
            return self.manejar_excepcion(e, "Error al procesar el restablecimiento")
        finally:
            if not self.session:
                db.close()

    def validar_token_restablecimiento(self, token):
        db = self.get_db_session()
        try:
            usuario = db.query(Usuario).filter(Usuario.reset_token == token).first()
            if usuario and usuario.reset_token_expiry and usuario.reset_token_expiry > datetime.now():
                return usuario
            return None
        finally:
            if not self.session:
                db.close()

    def restablecer_contrasena(self, token, nueva_contrasena):
        db = self.get_db_session()
        try:
            usuario = self.validar_token_restablecimiento(token)
            if not usuario:
                return False, "El enlace es inválido o ha expirado."
            
            usuario.password = Usuario.hash_password(nueva_contrasena)
            usuario.reset_token = None
            usuario.reset_token_expiry = None
            db.commit()
            return True, "Contraseña actualizada correctamente."
        except SQLAlchemyError as e:
            db.rollback()
            return self.manejar_excepcion(e, "Error al actualizar la contraseña")
        finally:
            if not self.session:
                db.close()
