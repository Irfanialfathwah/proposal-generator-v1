"""Relation proposal_product 2

Revision ID: e931fa2483fb
Revises: 21a77b587f36
Create Date: 2021-07-05 09:52:07.208260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e931fa2483fb'
down_revision = '21a77b587f36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proposal_products',
    sa.Column('proposal_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposals.id'], ),
    sa.PrimaryKeyConstraint('proposal_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('proposal_products')
    # ### end Alembic commands ###