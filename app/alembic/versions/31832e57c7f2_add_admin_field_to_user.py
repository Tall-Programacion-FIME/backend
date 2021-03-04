"""Add admin field to user

Revision ID: 31832e57c7f2
Revises: 6478173b7f5d
Create Date: 2021-03-04 16:49:00.620680

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '31832e57c7f2'
down_revision = '6478173b7f5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.execute("UPDATE users SET is_admin = false")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###