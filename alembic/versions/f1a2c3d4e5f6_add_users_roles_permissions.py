"""Add users, roles and permissions

Revision ID: f1a2c3d4e5f6
Revises: d4e7a7b9c2c1
Create Date: 2026-04-28 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2c3d4e5f6'
down_revision: Union[str, None] = 'd4e7a7b9c2c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        sa.UniqueConstraint('nombre', name='uq_roles_nombre'),
    )
    op.create_index('ix_roles_nombre', 'roles', ['nombre'], unique=True)

    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('codigo', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=True),
        sa.UniqueConstraint('codigo', name='uq_permissions_codigo'),
    )
    op.create_index('ix_permissions_codigo', 'permissions', ['codigo'], unique=True)

    op.create_table(
        'role_permissions',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=60), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('creado_en', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('rol_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['rol_id'], ['roles.id']),
        sa.UniqueConstraint('username', name='uq_usuarios_username'),
    )
    op.create_index('ix_usuarios_username', 'usuarios', ['username'], unique=True)
    op.create_index('ix_usuarios_rol_id', 'usuarios', ['rol_id'], unique=False)

    roles_table = sa.table(
        'roles',
        sa.column('id', sa.Integer),
        sa.column('nombre', sa.String),
        sa.column('descripcion', sa.String),
    )

    permissions_table = sa.table(
        'permissions',
        sa.column('id', sa.Integer),
        sa.column('codigo', sa.String),
        sa.column('descripcion', sa.String),
    )

    role_permissions_table = sa.table(
        'role_permissions',
        sa.column('role_id', sa.Integer),
        sa.column('permission_id', sa.Integer),
    )

    usuarios_table = sa.table(
        'usuarios',
        sa.column('username', sa.String),
        sa.column('password', sa.String),
        sa.column('activo', sa.Boolean),
        sa.column('rol_id', sa.Integer),
    )

    role_rows = [
        {'id': 1, 'nombre': 'root', 'descripcion': 'Super usuario con acceso total'},
        {'id': 2, 'nombre': 'administrador', 'descripcion': 'Admin general sin gestion de usuarios'},
        {'id': 3, 'nombre': 'maestro', 'descripcion': 'Gestion de aulas y estadisticas'},
        {'id': 4, 'nombre': 'distribuidor', 'descripcion': 'Gestion de donaciones, preparados y distribucion'},
    ]
    op.bulk_insert(roles_table, role_rows)

    permission_codes = [
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
        'users.manage',
    ]
    permission_rows = [
        {'id': idx + 1, 'codigo': code, 'descripcion': f'Permiso {code}'}
        for idx, code in enumerate(permission_codes)
    ]
    op.bulk_insert(permissions_table, permission_rows)

    admin_permission_codes = [
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
    ]
    maestro_permission_codes = [
        'salones.view',
        'aulas.view', 'aulas.manage',
        'estadistica.view',
    ]
    distribuidor_permission_codes = [
        'aulas.view',
        'estadistica.view',
        'donaciones.view', 'donaciones.manage',
        'preparados.view', 'preparados.manage',
        'distribuciones.view', 'distribuciones.manage',
    ]

    perm_id_by_code = {row['codigo']: row['id'] for row in permission_rows}
    role_perm_rows = []

    for code in permission_codes:
        role_perm_rows.append({'role_id': 1, 'permission_id': perm_id_by_code[code]})

    for code in admin_permission_codes:
        role_perm_rows.append({'role_id': 2, 'permission_id': perm_id_by_code[code]})

    for code in maestro_permission_codes:
        role_perm_rows.append({'role_id': 3, 'permission_id': perm_id_by_code[code]})

    for code in distribuidor_permission_codes:
        role_perm_rows.append({'role_id': 4, 'permission_id': perm_id_by_code[code]})

    op.bulk_insert(role_permissions_table, role_perm_rows)

    op.bulk_insert(
        usuarios_table,
        [
            {'username': 'root', 'password': 'root123', 'activo': True, 'rol_id': 1},
            {'username': 'admin', 'password': 'admin123', 'activo': True, 'rol_id': 2},
        ],
    )


def downgrade() -> None:
    op.drop_index('ix_usuarios_rol_id', table_name='usuarios')
    op.drop_index('ix_usuarios_username', table_name='usuarios')
    op.drop_table('usuarios')

    op.drop_table('role_permissions')

    op.drop_index('ix_permissions_codigo', table_name='permissions')
    op.drop_table('permissions')

    op.drop_index('ix_roles_nombre', table_name='roles')
    op.drop_table('roles')
