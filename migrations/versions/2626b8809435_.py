"""empty message

Revision ID: 2626b8809435
Revises: 
Create Date: 2019-12-11 12:35:50.493796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2626b8809435'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'accessories', ['desc'])
    op.create_unique_constraint(None, 'other_materials', ['desc'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'other_materials', type_='unique')
    op.drop_constraint(None, 'accessories', type_='unique')
    # ### end Alembic commands ###
