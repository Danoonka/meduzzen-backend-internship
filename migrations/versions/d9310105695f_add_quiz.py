"""Add Quiz

Revision ID: d9310105695f
Revises: 159acb3b69d4
Create Date: 2023-08-09 22:57:10.403683

"""
from alembic import op
import sqlalchemy as sa


revision = 'd9310105695f'
down_revision = '159acb3b69d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('quizzes',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('quiz_name', sa.String(), nullable=True),
    sa.Column('quiz_title', sa.String(), nullable=True),
    sa.Column('quiz_description', sa.String(), nullable=True),
    sa.Column('quiz_frequency', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('quiz_id')
    )
    op.create_index(op.f('ix_quizzes_quiz_id'), 'quizzes', ['quiz_id'], unique=False)
    op.create_table('questions',
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.String(), nullable=True),
    sa.Column('question_answers', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('question_correct_answer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.quiz_id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_index(op.f('ix_questions_question_id'), 'questions', ['question_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_questions_question_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_quizzes_quiz_id'), table_name='quizzes')
    op.drop_table('quizzes')
