"""empty message

Revision ID: ceba231af8bd
Revises: 48254f8580d6
Create Date: 2024-07-09 02:34:21.636375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceba231af8bd'
down_revision = '48254f8580d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chambre_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_debut', sa.Date(), nullable=False),
    sa.Column('date_fin', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['chambre_id'], ['chambre.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_register.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    # ### end Alembic commands ###
