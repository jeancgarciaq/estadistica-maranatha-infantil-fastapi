"""Drop legacy donaciones_componentes table

Revision ID: d3f7a9e2c115
Revises: b2c4e8d1f501
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f7a9e2c115'
down_revision: Union[str, None] = 'b2c4e8d1f501'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('donaciones_componentes')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'donaciones_componentes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('donacion_compuesta_id', sa.Integer(), nullable=False),
        sa.Column('donacion_materia_id', sa.Integer(), nullable=False),
        sa.Column('cantidad_usada', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['donacion_compuesta_id'], ['donaciones.id']),
        sa.ForeignKeyConstraint(['donacion_materia_id'], ['donaciones.id']),
        sa.PrimaryKeyConstraint('id')
    )
