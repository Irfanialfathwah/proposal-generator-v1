"""add bid number table

Revision ID: 512f38e28c30
Revises: dfc018e13dc0
Create Date: 2021-07-12 08:58:37.998438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '512f38e28c30'
down_revision = 'dfc018e13dc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposals', 'bid_no')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('bid_no', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
