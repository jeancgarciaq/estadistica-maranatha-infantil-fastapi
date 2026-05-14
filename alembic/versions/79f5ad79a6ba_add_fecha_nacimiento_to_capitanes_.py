"""add_fecha_nacimiento_to_capitanes_coordinadores_lideres

Revision ID: 79f5ad79a6ba
Revises: 1c588da2442d
Create Date: 2026-05-14 15:08:55.728011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79f5ad79a6ba'
down_revision: Union[str, None] = '1c588da2442d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Añadir fecha_nacimiento y cambiar edad a Integer en capitanes
    with op.batch_alter_table('capitanes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_nacimiento', sa.Date(), nullable=True))
        batch_op.alter_column('edad',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using='edad::integer')

    # Añadir fecha_nacimiento y cambiar edad a Integer en coordinadores
    with op.batch_alter_table('coordinadores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_nacimiento', sa.Date(), nullable=True))
        batch_op.alter_column('edad',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using='edad::integer')

    # Añadir fecha_nacimiento y cambiar edad a Integer en lideres
    with op.batch_alter_table('lideres', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_nacimiento', sa.Date(), nullable=True))
        batch_op.alter_column('edad',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using='edad::integer')

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('lideres', schema=None) as batch_op:
        batch_op.alter_column('edad',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('fecha_nacimiento')

    with op.batch_alter_table('coordinadores', schema=None) as batch_op:
        batch_op.alter_column('edad',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('fecha_nacimiento')

    with op.batch_alter_table('capitanes', schema=None) as batch_op:
        batch_op.alter_column('edad',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('fecha_nacimiento')
