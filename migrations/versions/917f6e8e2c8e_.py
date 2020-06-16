"""empty message

Revision ID: 917f6e8e2c8e
Revises: 25a6ab26a6c7
Create Date: 2020-05-11 16:04:31.430235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '917f6e8e2c8e'
down_revision = '25a6ab26a6c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('_password', sa.String(length=150), nullable=False))
    op.drop_column('cms_user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('password', mysql.VARCHAR(length=150), nullable=False))
    op.drop_column('cms_user', '_password')
    # ### end Alembic commands ###
