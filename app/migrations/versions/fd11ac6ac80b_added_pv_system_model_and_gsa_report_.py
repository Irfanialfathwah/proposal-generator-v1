"""added pv_system model and gsa_report file column

Revision ID: fd11ac6ac80b
Revises: 262f45159646
Create Date: 2020-11-12 14:46:53.865946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd11ac6ac80b'
down_revision = '262f45159646'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposals', sa.Column('pv_system_model', sa.String(length=30), nullable=True))
    op.add_column('roofs', sa.Column('gsa_report_file', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roofs', 'gsa_report_file')
    op.drop_column('proposals', 'pv_system_model')
    # ### end Alembic commands ###