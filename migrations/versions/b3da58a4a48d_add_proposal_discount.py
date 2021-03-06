"""add proposal.discount

Revision ID: b3da58a4a48d
Revises: 56ca4ea31125
Create Date: 2021-04-16 07:40:59.473357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3da58a4a48d'
down_revision = '56ca4ea31125'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('discount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposals', 'discount')
    # ### end Alembic commands ###
