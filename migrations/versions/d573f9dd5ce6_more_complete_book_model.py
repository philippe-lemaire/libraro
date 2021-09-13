"""more complete book model

Revision ID: d573f9dd5ce6
Revises: 39b495ebce8f
Create Date: 2021-09-13 15:16:44.680568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd573f9dd5ce6'
down_revision = '39b495ebce8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('isbn13', sa.String(length=64), nullable=True))
    op.add_column('books', sa.Column('title', sa.String(length=128), nullable=True))
    op.add_column('books', sa.Column('authors', sa.String(length=128), nullable=True))
    op.add_column('books', sa.Column('publisher', sa.String(length=128), nullable=True))
    op.add_column('books', sa.Column('year', sa.String(length=64), nullable=True))
    op.add_column('books', sa.Column('language', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'language')
    op.drop_column('books', 'year')
    op.drop_column('books', 'publisher')
    op.drop_column('books', 'authors')
    op.drop_column('books', 'title')
    op.drop_column('books', 'isbn13')
    # ### end Alembic commands ###