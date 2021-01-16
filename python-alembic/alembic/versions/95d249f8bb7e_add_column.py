"""add column

Revision ID: 95d249f8bb7e
Revises: 605c309b04e0
Create Date: 2020-12-27 00:55:47.198154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95d249f8bb7e'
down_revision = '605c309b04e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('age', sa.Float))


def downgrade():
    op.drop_column('user', 'age')
