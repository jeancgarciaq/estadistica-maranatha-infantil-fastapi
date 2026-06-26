"""create_models

Revision ID: 3b8010f0a934
Revises: bca6ad158e56
Create Date: 2026-06-25 19:38:55.265536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b8010f0a934'
down_revision: Union[str, None] = 'bca6ad158e56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Las tablas ya existen desde la migración inicial ad5a6de3a358.
    # Esta migración es un no-op para evitar errores de CREATE TABLE en tablas existentes.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
