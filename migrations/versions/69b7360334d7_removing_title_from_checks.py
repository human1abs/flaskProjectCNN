"""Removing Title from checks

Revision ID: 69b7360334d7
Revises: dc4e82a8c15a
Create Date: 2024-11-13 19:32:21.783110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b7360334d7'
down_revision = 'dc4e82a8c15a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('checks', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('checks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False))

    # ### end Alembic commands ###