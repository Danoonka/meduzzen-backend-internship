"""Change type

Revision ID: 5f6af13a3205
Revises: 7c1ca21d0c27
Create Date: 2023-08-17 00:22:49.185256

"""
from alembic import op
import sqlalchemy as sa

revision = '5f6af13a3205'
down_revision = '7c1ca21d0c27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('ix_answers_answer_id', table_name='answers')
    op.create_index(op.f('ix_answers_answer_id'), 'answers', ['answer_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_answers_answer_id'), table_name='answers')
    op.create_index('ix_answers_answer_id', 'answers', ['answer_id'], unique=False)
