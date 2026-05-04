from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.database import Base
from models.base_class import AuditMixin


ROLE_ROOT = 'root'
ROLE_ADMIN = 'administrador'
ROLE_MAESTRO = 'maestro'
ROLE_DISTRIBUIDOR = 'distribuidor'


DEFAULT_ROLE_PERMISSIONS = {
    ROLE_ROOT: ['*'],
    ROLE_ADMIN: [
        'areas.view', 'areas.manage',
        'salones.view', 'salones.manage',
        'aulas.view', 'aulas.manage',
        'estadistica.view',
        'donaciones.view', 'donaciones.manage',
        'preparados.view', 'preparados.manage',
        'distribuciones.view', 'distribuciones.manage',
        'logistica.view', 'logistica.manage',
        'otras_areas.view', 'otras_areas.manage',
        'ensenanza.view', 'ensenanza.manage',
        'recepcion.view', 'recepcion.manage',
        'reporte.view',
        'ayuda.view',
    ],
    ROLE_MAESTRO: [
        'salones.view',
        'aulas.view', 'aulas.manage',
        'estadistica.view',
    ],
    ROLE_DISTRIBUIDOR: [
        'aulas.view',
        'estadistica.view',
        'donaciones.view', 'donaciones.manage',
        'preparados.view', 'preparados.manage',
        'distribuciones.view', 'distribuciones.manage',
    ],
}


role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
)


class Rol(Base, AuditMixin):
    __tablename__ = 'roles'

    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    usuarios = relationship('Usuario', back_populates='rol')
    permisos = relationship('Permiso', secondary=role_permissions, back_populates='roles')

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"


class Permiso(Base, AuditMixin):
    __tablename__ = 'permissions'

    codigo = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    roles = relationship('Rol', secondary=role_permissions, back_populates='permisos')

    def __repr__(self):
        return f"<Permiso(id={self.id}, codigo='{self.codigo}')>"


class Usuario(Base, AuditMixin):
    __tablename__ = 'usuarios'

    username = Column(String(60), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    
    # Campos para recuperación de contraseña
    reset_token = Column(String(100), nullable=True, index=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    rol = relationship('Rol', back_populates='usuarios')

    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}', rol_id={self.rol_id})>"

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)


def seed_security_data(session):
    """Create default roles, permissions and bootstrap users if they do not exist."""
    role_objects = {}

    for role_name, role_permissions_codes in DEFAULT_ROLE_PERMISSIONS.items():
        role = session.query(Rol).filter(Rol.nombre == role_name).first()
        if role is None:
            role = Rol(nombre=role_name, descripcion=f'Rol del sistema: {role_name}')
            session.add(role)
            session.flush()
        role_objects[role_name] = role

        if '*' in role_permissions_codes:
            continue

        permisos_actuales = {perm.codigo: perm for perm in role.permisos}
        for code in role_permissions_codes:
            permiso = session.query(Permiso).filter(Permiso.codigo == code).first()
            if permiso is None:
                permiso = Permiso(codigo=code, descripcion=f'Permiso {code}')
                session.add(permiso)
                session.flush()
            if code not in permisos_actuales:
                role.permisos.append(permiso)

    root_role = role_objects[ROLE_ROOT]

    root_user = session.query(Usuario).filter(Usuario.username == 'root').first()
    if root_user is None:
        # Contraseña por defecto: root123 (Se recomienda cambiar al primer inicio)
        hashed_pw = Usuario.hash_password('root123')
        session.add(Usuario(username='root', password=hashed_pw, rol_id=root_role.id, activo=True))
    
    session.commit()
