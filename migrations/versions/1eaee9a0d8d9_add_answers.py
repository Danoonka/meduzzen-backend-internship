"""Add answers

Revision ID: 1eaee9a0d8d9
Revises: 68fdce225053
Create Date: 2023-08-16 18:21:30.426837

"""
from alembic import op
import sqlalchemy as sa

revision = '1eaee9a0d8d9'
down_revision = '68fdce225053'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('answers',
                    sa.Column('answer_id', sa.Integer(), nullable=False),
                    sa.Column('quiz_id', sa.Integer(), nullable=True),
                    sa.Column('answers', sa.ARRAY(sa.String()), nullable=True),
                    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
                    sa.PrimaryKeyConstraint('answer_id')
                    )
    op.create_index(op.f('ix_answers_answer_id'), 'answers', ['answer_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_answers_answer_id'), table_name='answers')
    op.drop_table('answers')
