"""Drop servidores table

Revision ID: 20240520120000
Revises: 751a47a06aaa
Create Date: 2024-05-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20240520120000'
down_revision = '751a47a06aaa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Eliminar tabla 'servidores' de forma segura en SQLite y PostgreSQL
    op.execute('DROP TABLE IF EXISTS servidores CASCADE')


def downgrade() -> None:
    # No se restaura la tabla: eliminación definitiva
    pass
