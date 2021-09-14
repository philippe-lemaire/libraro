"""added index true on user.email and flask login mixin

Revision ID: 1d6088378e38
Revises: 91ad65017758
Create Date: 2021-09-13 16:18:17.564825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d6088378e38'
down_revision = '91ad65017758'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    # ### end Alembic commands ###
