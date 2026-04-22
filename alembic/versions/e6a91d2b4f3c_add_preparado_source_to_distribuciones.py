"""Add prepared source to distribuciones

Revision ID: e6a91d2b4f3c
Revises: d3f7a9e2c115
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6a91d2b4f3c'
down_revision: Union[str, None] = 'd3f7a9e2c115'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alimento_preparado_id', sa.Integer(), nullable=True))
        batch_op.alter_column('donacion_id', existing_type=sa.INTEGER(), nullable=True)
        batch_op.create_foreign_key(
            'fk_distribuciones_alimento_preparado_id_alimentos_preparados',
            'alimentos_preparados',
            ['alimento_preparado_id'],
            ['id']
        )
        batch_op.drop_constraint('ck_distribuciones_destino_unico', type_='check')
        batch_op.create_check_constraint(
            'ck_distribuciones_destino_unico',
            '(salon_id IS NOT NULL AND area_id IS NULL) OR (salon_id IS NULL AND area_id IS NOT NULL)'
        )
        batch_op.create_check_constraint(
            'ck_distribuciones_origen_unico',
            '(donacion_id IS NOT NULL AND alimento_preparado_id IS NULL) OR (donacion_id IS NULL AND alimento_preparado_id IS NOT NULL)'
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.drop_constraint('ck_distribuciones_origen_unico', type_='check')
        batch_op.drop_constraint('ck_distribuciones_destino_unico', type_='check')
        batch_op.create_check_constraint(
            'ck_distribuciones_destino_unico',
            '(salon_id IS NOT NULL AND area_id IS NULL) OR (salon_id IS NULL AND area_id IS NOT NULL)'
        )
        batch_op.drop_constraint('fk_distribuciones_alimento_preparado_id_alimentos_preparados', type_='foreignkey')
        batch_op.alter_column('donacion_id', existing_type=sa.INTEGER(), nullable=False)
        batch_op.drop_column('alimento_preparado_id')
