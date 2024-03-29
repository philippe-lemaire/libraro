"""book cover

Revision ID: 97dc57f320e9
Revises: 54e71a2dfc8a
Create Date: 2021-10-15 14:36:44.644140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97dc57f320e9"
down_revision = "54e71a2dfc8a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('books', 'user_review')
    op.add_column("books", sa.Column("cover", sa.VARCHAR(length=256), nullable=True))
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("books", sa.Column("cover", sa.VARCHAR(length=256), nullable=True))
    # ### end Alembic commands ###
    pass
