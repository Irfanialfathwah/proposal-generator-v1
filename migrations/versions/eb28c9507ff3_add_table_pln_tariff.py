"""add table pln_tariff

Revision ID: eb28c9507ff3
Revises: 7358bbf0d03d
Create Date: 2021-04-23 10:54:55.549199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb28c9507ff3'
down_revision = '7358bbf0d03d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposals', 'pln_price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('pln_price', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###