"""empty message

Revision ID: 0cbdb0f95486
Revises: 
Create Date: 2017-07-13 10:06:11.559909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cbdb0f95486'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bucketlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=25), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucketlists')
    # ### end Alembic commands ###