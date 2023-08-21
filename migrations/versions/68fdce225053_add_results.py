"""Add results

Revision ID: 68fdce225053
Revises: d9310105695f
Create Date: 2023-08-16 17:33:34.089768

"""
from alembic import op
import sqlalchemy as sa

revision = '68fdce225053'
down_revision = 'd9310105695f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('results',
                    sa.Column('result_id', sa.Integer(), nullable=False),
                    sa.Column('score', sa.Float(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('quiz_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
                    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('result_id')
                    )
    op.create_index(op.f('ix_results_result_id'), 'results', ['result_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_results_result_id'), table_name='results')
    op.drop_table('results')
