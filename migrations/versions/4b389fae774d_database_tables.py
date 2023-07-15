"""DAtabase tables

Revision ID: 4b389fae774d
Revises: 
Create Date: 2023-07-15 23:28:16.424862

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4b389fae774d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('user_email', sa.String(), nullable=False),
                    sa.Column('user_firstname', sa.String(), nullable=False),
                    sa.Column('user_lastname', sa.String(), nullable=False),
                    sa.Column('user_avatar', sa.String(), nullable=True),
                    sa.Column('user_status', sa.String(), nullable=True),
                    sa.Column('user_city', sa.String(), nullable=True),
                    sa.Column('user_phone', sa.Integer(), nullable=True),
                    sa.Column('is_superuser', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('user_id')
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
    op.drop_table('users')
