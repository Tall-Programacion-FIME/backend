"""Add price field to book table

Revision ID: 2fd423e65ebe
Revises: 31832e57c7f2
Create Date: 2021-03-05 15:30:03.252455

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2fd423e65ebe"
down_revision = "31832e57c7f2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("books", sa.Column("price", sa.Numeric(), nullable=False))
    op.execute("UPDATE books SET price = 0")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("books", "price")
    # ### end Alembic commands ###
