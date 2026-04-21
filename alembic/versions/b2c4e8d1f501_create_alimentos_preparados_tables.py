"""Create alimentos preparados tables

Revision ID: b2c4e8d1f501
Revises: a1f3d9c4b210
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c4e8d1f501'
down_revision: Union[str, None] = 'a1f3d9c4b210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'alimentos_preparados',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('descripcion', sa.String(length=255), nullable=False),
        sa.Column('cantidad', sa.Float(), nullable=False),
        sa.Column('unidad', sa.String(length=50), nullable=False),
        sa.Column('equipo', sa.String(length=100), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'alimentos_preparados_componentes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('alimento_preparado_id', sa.Integer(), nullable=False),
        sa.Column('donacion_materia_id', sa.Integer(), nullable=False),
        sa.Column('cantidad_usada', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['alimento_preparado_id'], ['alimentos_preparados.id']),
        sa.ForeignKeyConstraint(['donacion_materia_id'], ['donaciones.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('alimentos_preparados_componentes')
    op.drop_table('alimentos_preparados')
