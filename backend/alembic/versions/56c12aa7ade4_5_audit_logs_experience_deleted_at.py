"""Audit logs table, experience_years precision, skill soft delete

Revision ID: 56c12aa7ade4
Revises: 45b007426523
Create Date: 2026-09-01 21:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '56c12aa7ade4'
down_revision: Union[str, Sequence[str], None] = '45b007426523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('old_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('new_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'], unique=False)
    op.create_index('ix_audit_logs_entity_type', 'audit_logs', ['entity_type'], unique=False)

    # Alter experience_years precision for employees and job_postings
    op.alter_column('employees', 'experience_years',
               existing_type=sa.NUMERIC(precision=2, scale=2),
               type_=sa.DECIMAL(precision=4, scale=2),
               existing_nullable=False)

    op.alter_column('job_postings', 'experience_years',
               existing_type=sa.NUMERIC(precision=2, scale=2),
               type_=sa.DECIMAL(precision=4, scale=2),
               existing_nullable=False)

    # Add deleted_at to skills
    op.add_column('skills', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('skills', 'deleted_at')
    
    op.alter_column('job_postings', 'experience_years',
               existing_type=sa.DECIMAL(precision=4, scale=2),
               type_=sa.NUMERIC(precision=2, scale=2),
               existing_nullable=False)

    op.alter_column('employees', 'experience_years',
               existing_type=sa.DECIMAL(precision=4, scale=2),
               type_=sa.NUMERIC(precision=2, scale=2),
               existing_nullable=False)

    op.drop_index('ix_audit_logs_entity_type', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_id', table_name='audit_logs')
    op.drop_table('audit_logs')
