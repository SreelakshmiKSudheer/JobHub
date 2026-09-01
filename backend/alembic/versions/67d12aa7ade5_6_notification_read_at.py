"""Add read_at to notifications table

Revision ID: 67d12aa7ade5
Revises: 56c12aa7ade4
Create Date: 2026-09-01 21:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '67d12aa7ade5'
down_revision: Union[str, Sequence[str], None] = '56c12aa7ade4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('notifications', sa.Column('read_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('notifications', 'read_at')
