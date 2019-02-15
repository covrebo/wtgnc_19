"""Added a 4th driver to the weekly picks table

Revision ID: 7092042b3be5
Revises: f8086dc81122
Create Date: 2019-02-15 17:19:06.889411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7092042b3be5'
down_revision = 'f8086dc81122'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pick', sa.Column('driver_4', sa.String(length=30), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pick', 'driver_4')
    # ### end Alembic commands ###
