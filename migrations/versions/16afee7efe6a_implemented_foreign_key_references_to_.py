"""Implemented foreign key references to week columns

Revision ID: 16afee7efe6a
Revises: ee5891f000fd
Create Date: 2019-02-09 18:33:07.713797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16afee7efe6a'
down_revision = 'ee5891f000fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('driver', sa.Column('week', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'driver', 'event', ['week'], ['id'])
    op.drop_column('driver', 'week_str')
    op.drop_column('driver', 'week_id')
    op.add_column('pick', sa.Column('week', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'pick', 'event', ['week'], ['id'])
    op.drop_column('pick', 'week_str')
    op.drop_column('pick', 'week_id')
    op.add_column('result', sa.Column('week', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'result', 'event', ['week'], ['id'])
    op.drop_column('result', 'week_str')
    op.drop_column('result', 'week_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('week_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('result', sa.Column('week_str', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'result', type_='foreignkey')
    op.drop_column('result', 'week')
    op.add_column('pick', sa.Column('week_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('pick', sa.Column('week_str', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'pick', type_='foreignkey')
    op.drop_column('pick', 'week')
    op.add_column('driver', sa.Column('week_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('driver', sa.Column('week_str', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'driver', type_='foreignkey')
    op.drop_column('driver', 'week')
    # ### end Alembic commands ###
