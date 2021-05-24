"""add table pln_tariff 2

Revision ID: b8ff7afaeeb4
Revises: eb28c9507ff3
Create Date: 2021-04-23 11:11:52.262545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8ff7afaeeb4'
down_revision = 'eb28c9507ff3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pln_tariffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pln_tariff_group', sa.String(length=100), nullable=True),
    sa.Column('pln_price', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pln_tariffs')
    # ### end Alembic commands ###