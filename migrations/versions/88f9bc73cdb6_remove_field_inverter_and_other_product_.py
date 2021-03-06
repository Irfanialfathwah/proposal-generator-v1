"""remove field inverter and other product in proposal table

Revision ID: 88f9bc73cdb6
Revises: 6f6f79851f79
Create Date: 2021-07-07 15:30:41.550614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88f9bc73cdb6'
down_revision = '6f6f79851f79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposals', 'inverter_stg3')
    op.drop_column('proposals', 'energy_accounting_system')
    op.drop_column('proposals', 'inverter_stg6')
    op.drop_column('proposals', 'inverter_stg20')
    op.drop_column('proposals', 'inverter_stg125')
    op.drop_column('proposals', 'inverter_stg250')
    op.drop_column('proposals', 'inverter_stg60')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('inverter_stg60', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('inverter_stg250', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('inverter_stg125', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('inverter_stg20', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('inverter_stg6', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('energy_accounting_system', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('proposals', sa.Column('inverter_stg3', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
