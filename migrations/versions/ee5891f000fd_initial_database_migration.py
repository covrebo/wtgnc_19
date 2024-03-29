"""Initial database migration

Revision ID: ee5891f000fd
Revises: 
Create Date: 2019-02-09 17:54:12.900068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee5891f000fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('week_str', sa.String(length=30), nullable=False),
    sa.Column('car_number', sa.Integer(), nullable=False),
    sa.Column('driver', sa.String(length=30), nullable=False),
    sa.Column('sponsor', sa.String(length=30), nullable=False),
    sa.Column('make', sa.String(length=10), nullable=False),
    sa.Column('team', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('week_str', sa.String(length=30), nullable=False),
    sa.Column('track', sa.String(length=30), nullable=False),
    sa.Column('race', sa.String(length=30), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('make',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pick',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('week_str', sa.String(length=30), nullable=False),
    sa.Column('display_name', sa.String(length=30), nullable=False),
    sa.Column('driver_1', sa.String(length=30), nullable=False),
    sa.Column('driver_2', sa.String(length=30), nullable=False),
    sa.Column('driver_3', sa.String(length=30), nullable=False),
    sa.Column('make', sa.String(length=10), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('week_str', sa.String(length=30), nullable=False),
    sa.Column('car_number', sa.Integer(), nullable=False),
    sa.Column('driver', sa.String(length=30), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_first_name', sa.String(length=20), nullable=False),
    sa.Column('user_last_name', sa.String(length=20), nullable=False),
    sa.Column('display_name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('display_name'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('result')
    op.drop_table('pick')
    op.drop_table('make')
    op.drop_table('event')
    op.drop_table('driver')
    # ### end Alembic commands ###
