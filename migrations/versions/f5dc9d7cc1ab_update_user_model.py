"""Update user model

Revision ID: f5dc9d7cc1ab
Revises: 4b389fae774d
Create Date: 2023-07-17 22:55:24.821031

"""
from alembic import op
import sqlalchemy as sa

revision = 'f5dc9d7cc1ab'
down_revision = '4b389fae774d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('user_password', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'user_password')
