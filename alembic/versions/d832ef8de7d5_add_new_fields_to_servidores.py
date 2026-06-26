"""add_new_fields_to_servidores

Revision ID: d832ef8de7d5
Revises: 0812272a350b
Create Date: 2026-06-26 16:33:45.044926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd832ef8de7d5'
down_revision: Union[str, None] = '0812272a350b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('servidores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sexo', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('profesion', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('estado_civil', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('cantidad_hijos', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tiempo_servicio', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('pertenece_evangelio_cambia', sa.String(length=5), nullable=True))
        batch_op.add_column(sa.Column('sirve_otra_area', sa.String(length=5), nullable=True))
        batch_op.add_column(sa.Column('otra_area_detalle', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('bautizado', sa.String(length=5), nullable=True))
        batch_op.add_column(sa.Column('asiste_discipulado', sa.String(length=5), nullable=True))
        batch_op.add_column(sa.Column('usa_transporte', sa.String(length=5), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('servidores', schema=None) as batch_op:
        batch_op.drop_column('usa_transporte')
        batch_op.drop_column('asiste_discipulado')
        batch_op.drop_column('bautizado')
        batch_op.drop_column('otra_area_detalle')
        batch_op.drop_column('sirve_otra_area')
        batch_op.drop_column('pertenece_evangelio_cambia')
        batch_op.drop_column('tiempo_servicio')
        batch_op.drop_column('cantidad_hijos')
        batch_op.drop_column('estado_civil')
        batch_op.drop_column('profesion')
        batch_op.drop_column('sexo')
