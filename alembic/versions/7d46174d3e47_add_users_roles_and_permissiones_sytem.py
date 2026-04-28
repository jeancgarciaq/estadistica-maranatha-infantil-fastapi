"""Add users, roles and permissiones sytem

Revision ID: 7d46174d3e47
Revises: f1a2c3d4e5f6
Create Date: 2026-04-28 12:38:07.538620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d46174d3e47'
down_revision: Union[str, None] = 'f1a2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
