"""Add recepcion destination to distribuciones

Revision ID: d4e7a7b9c2c1
Revises: e6a91d2b4f3c
Create Date: 2026-04-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e7a7b9c2c1'
down_revision: Union[str, None] = 'e6a91d2b4f3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recepcion_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_distribuciones_recepcion_id_recepciones',
            'recepciones',
            ['recepcion_id'],
            ['id']
        )
        batch_op.drop_constraint('ck_distribuciones_destino_unico', type_='check')
        batch_op.create_check_constraint(
            'ck_distribuciones_destino_unico',
            '(salon_id IS NOT NULL AND area_id IS NULL AND recepcion_id IS NULL) OR '
            '(salon_id IS NULL AND area_id IS NOT NULL AND recepcion_id IS NULL) OR '
            '(salon_id IS NULL AND area_id IS NULL AND recepcion_id IS NOT NULL)'
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('distribuciones', schema=None) as batch_op:
        batch_op.drop_constraint('ck_distribuciones_destino_unico', type_='check')
        batch_op.create_check_constraint(
            'ck_distribuciones_destino_unico',
            '(salon_id IS NOT NULL AND area_id IS NULL) OR (salon_id IS NULL AND area_id IS NOT NULL)'
        )
        batch_op.drop_constraint('fk_distribuciones_recepcion_id_recepciones', type_='foreignkey')
        batch_op.drop_column('recepcion_id')