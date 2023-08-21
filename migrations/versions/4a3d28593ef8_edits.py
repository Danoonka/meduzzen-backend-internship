"""Edits

Revision ID: 4a3d28593ef8
Revises: 5f6af13a3205
Create Date: 2023-08-17 00:42:26.219762

"""
from alembic import op
import sqlalchemy as sa

revision = '4a3d28593ef8'
down_revision = '5f6af13a3205'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('ix_answers_answer_id', table_name='answers')
    op.create_index(op.f('ix_answers_answer_id'), 'answers', ['answer_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_answers_answer_id'), table_name='answers')
    op.create_index('ix_answers_answer_id', 'answers', ['answer_id'], unique=False)
