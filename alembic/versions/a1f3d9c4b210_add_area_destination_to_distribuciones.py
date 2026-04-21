"""Add area destination to distribuciones

Revision ID: a1f3d9c4b210
Revises: 49dcd44ce334
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1f3d9c4b210'
down_revision: Union[str, None] = '49dcd44ce334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('area_id', sa.Integer(), nullable=True))
        batch_op.alter_column('salon_id', existing_type=sa.INTEGER(), nullable=True)
        batch_op.create_foreign_key(
            'fk_distribuciones_area_id_areas',
            'areas',
            ['area_id'],
            ['id']
        )
        batch_op.create_check_constraint(
            'ck_distribuciones_destino_unico',
            '(salon_id IS NOT NULL AND area_id IS NULL) OR (salon_id IS NULL AND area_id IS NOT NULL)'
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.drop_constraint('ck_distribuciones_destino_unico', type_='check')
        batch_op.drop_constraint('fk_distribuciones_area_id_areas', type_='foreignkey')
        batch_op.drop_column('area_id')
        batch_op.alter_column('salon_id', existing_type=sa.INTEGER(), nullable=False)
