"""create tables

Revision ID: 159acb3b69d4
Revises: 
Create Date: 2023-08-04 11:55:02.765451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '159acb3b69d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('companies',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('company_description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('company_visible', sa.Boolean(), nullable=True),
    sa.Column('company_avatar', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('company_id')
    )
    op.create_index(op.f('ix_companies_company_id'), 'companies', ['company_id'], unique=False)
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(), nullable=False),
    sa.Column('user_firstname', sa.String(), nullable=False),
    sa.Column('user_lastname', sa.String(), nullable=False),
    sa.Column('user_avatar', sa.String(), nullable=True),
    sa.Column('user_status', sa.String(), nullable=True),
    sa.Column('user_city', sa.String(), nullable=True),
    sa.Column('user_phone', sa.Integer(), nullable=True),
    sa.Column('user_password', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('actions',
    sa.Column('action_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('action_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('action_id')
    )
    op.create_table('user_links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('user_links')
    op.drop_table('actions')
    op.drop_table('users')
    op.drop_index(op.f('ix_companies_company_id'), table_name='companies')
    op.drop_table('companies')
