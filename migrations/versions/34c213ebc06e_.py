"""empty message

Revision ID: 34c213ebc06e
Revises: 5a935a7dd20c
Create Date: 2024-06-25 19:24:12.966203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c213ebc06e'
down_revision = '5a935a7dd20c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chambre', schema=None) as batch_op:
        batch_op.drop_constraint('chambre_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user_register', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chambre', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('chambre_user_id_fkey', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###