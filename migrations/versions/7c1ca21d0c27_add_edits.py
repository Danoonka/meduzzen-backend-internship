"""Add edits

Revision ID: 7c1ca21d0c27
Revises: 1eaee9a0d8d9
Create Date: 2023-08-16 23:48:21.640019

"""
from alembic import op
import sqlalchemy as sa

revision = '7c1ca21d0c27'
down_revision = '1eaee9a0d8d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('answers', sa.Column('result_id', sa.Integer(), nullable=True))
    op.drop_index('ix_answers_answer_id', table_name='answers')
    op.create_index(op.f('ix_answers_answer_id'), 'answers', ['answer_id'], unique=True)
    op.create_foreign_key(None, 'answers', 'results', ['result_id'], ['result_id'])


def downgrade() -> None:
    op.drop_constraint(None, 'answers', type_='foreignkey')
    op.drop_index(op.f('ix_answers_answer_id'), table_name='answers')
    op.create_index('ix_answers_answer_id', 'answers', ['answer_id'], unique=False)
    op.drop_column('answers', 'result_id')
