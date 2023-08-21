"""Add datetime column

Revision ID: 016aae3e5130
Revises: b2895328a945
Create Date: 2023-08-17 13:45:13.919500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '016aae3e5130'
down_revision = 'b2895328a945'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('results', sa.Column('passed_at', sa.DateTime(), nullable=True))



def downgrade() -> None:
    op.drop_column('results', 'passed_at')

