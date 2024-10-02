"""empty message

Revision ID: 48254f8580d6
Revises: 6dfe110ea0d8
Create Date: 2024-07-08 23:31:43.336996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48254f8580d6'
down_revision = '6dfe110ea0d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chambre', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chambre', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
