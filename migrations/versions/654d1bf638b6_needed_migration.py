"""needed migration?

Revision ID: 654d1bf638b6
Revises: 09ad562d6b27
Create Date: 2021-10-14 16:19:23.264603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654d1bf638b6'
down_revision = '09ad562d6b27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('books', sa.Column('to_trade', sa.Boolean(), nullable=True))
    #op.drop_constraint('users_email_key', 'users', type_='unique')
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('books', 'to_trade')
    # ### end Alembic commands ###
