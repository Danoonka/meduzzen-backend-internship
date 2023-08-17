"""Change result model

Revision ID: 7318091ed5a7
Revises: 016aae3e5130
Create Date: 2023-08-17 14:08:44.893953

"""
from alembic import op
import sqlalchemy as sa

revision = '7318091ed5a7'
down_revision = '016aae3e5130'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('results', sa.Column('right_answers', sa.Integer(), nullable=True))
    op.add_column('results', sa.Column('answers', sa.Integer(), nullable=True))
    op.drop_column('results', 'score')


def downgrade() -> None:
    op.add_column('results', sa.Column('score', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('results', 'answers')
    op.drop_column('results', 'right_answers')
