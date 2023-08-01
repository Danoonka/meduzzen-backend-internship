"""add avatar

Revision ID: bf432aad5bfc
Revises: 56a2880ea91e
Create Date: 2023-07-31 12:35:04.751429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf432aad5bfc'
down_revision = '56a2880ea91e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('companies', sa.Column('company_avatar', sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_column('companies', 'company_avatar')

