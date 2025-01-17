"""empty message

Revision ID: e949d5a6ddc7
Revises: 5c5288957a9f
Create Date: 2024-06-22 02:27:26.578674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e949d5a6ddc7'
down_revision = '5c5288957a9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_register', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verified', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_register', schema=None) as batch_op:
        batch_op.drop_column('verified')

    # ### end Alembic commands ###
