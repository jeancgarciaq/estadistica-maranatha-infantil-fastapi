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
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
