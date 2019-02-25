"""Added table to hold starting lineup data

Revision ID: 7c469ed02f7c
Revises: 515800272b10
Create Date: 2019-02-22 20:55:13.118327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c469ed02f7c'
down_revision = '515800272b10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starting_lineup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('car_number', sa.Integer(), nullable=False),
    sa.Column('driver', sa.String(length=30), nullable=False),
    sa.Column('team', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['week'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('starting_lineup')
    # ### end Alembic commands ###