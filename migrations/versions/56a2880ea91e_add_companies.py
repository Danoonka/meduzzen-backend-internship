"""add companies

Revision ID: 56a2880ea91e
Revises: f5dc9d7cc1ab
Create Date: 2023-07-31 11:29:47.548376

"""
from alembic import op
import sqlalchemy as sa

revision = '56a2880ea91e'
down_revision = 'f5dc9d7cc1ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('companies',
                    sa.Column('company_id', sa.Integer(), nullable=False),
                    sa.Column('company_name', sa.String(), nullable=True),
                    sa.Column('company_description', sa.String(), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=True),
                    sa.Column('company_visible', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('company_id')
                    )
    op.create_index(op.f('ix_companies_company_id'), 'companies', ['company_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_companies_company_id'), table_name='companies')
    op.drop_table('companies')
