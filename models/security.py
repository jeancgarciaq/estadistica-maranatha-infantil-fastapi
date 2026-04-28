from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.base import Base, SyncMixin


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


class Rol(SyncMixin, Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    usuarios = relationship('Usuario', back_populates='rol')
    permisos = relationship('Permiso', secondary=role_permissions, back_populates='roles')

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"


class Permiso(SyncMixin, Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)

    roles = relationship('Rol', secondary=role_permissions, back_populates='permisos')

    def __repr__(self):
        return f"<Permiso(id={self.id}, codigo='{self.codigo}')>"


class Usuario(SyncMixin, Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)

    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    rol = relationship('Rol', back_populates='usuarios')

    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}', rol_id={self.rol_id})>"


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
    admin_role = role_objects[ROLE_ADMIN]

    root_user = session.query(Usuario).filter(Usuario.username == 'root').first()
    if root_user is None:
        session.add(Usuario(username='root', password='root123', rol_id=root_role.id, activo=True))

    admin_user = session.query(Usuario).filter(Usuario.username == 'admin').first()
    if admin_user is None:
        session.add(Usuario(username='admin', password='admin123', rol_id=admin_role.id, activo=True))
