"""empty message

Revision ID: 7e3d4427b0e8
Revises: fd11ac6ac80b
Create Date: 2020-11-13 15:37:26.067386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3d4427b0e8'
down_revision = 'fd11ac6ac80b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('solarmonthdatas_year_id_fkey', 'solarmonthdatas', type_='foreignkey')
    op.drop_column('solarmonthdatas', 'year_id')
    op.drop_table('solaryeardatas')
    op.add_column('solarmonthdatas', sa.Column('roof_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'solarmonthdatas', 'roofs', ['roof_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('solarmonthdatas', sa.Column('year_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'solarmonthdatas', type_='foreignkey')
    op.create_foreign_key('solarmonthdatas_year_id_fkey', 'solarmonthdatas', 'solaryeardatas', ['year_id'], ['id'])
    op.drop_column('solarmonthdatas', 'roof_id')
    op.create_table('solaryeardatas',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('roof_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('energy', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['roof_id'], ['roofs.id'], name='solaryeardatas_roof_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='solaryeardatas_pkey')
    )
    # ### end Alembic commands ###