"""even more complete book model

Revision ID: 3e0455629290
Revises: d573f9dd5ce6
Create Date: 2021-09-13 15:38:06.285205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0455629290'
down_revision = 'd573f9dd5ce6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('last_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'last_updated')
    # ### end Alembic commands ###