"""add table pln_tariff 

Revision ID: b423af0632fe
Revises: b8ff7afaeeb4
Create Date: 2021-04-23 13:08:45.234187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b423af0632fe'
down_revision = 'b8ff7afaeeb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('pln_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposals', 'pln_price')
    # ### end Alembic commands ###
