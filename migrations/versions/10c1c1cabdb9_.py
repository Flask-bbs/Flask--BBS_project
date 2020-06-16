"""empty message

Revision ID: 10c1c1cabdb9
Revises: 556823bfe3a7
Create Date: 2020-05-21 17:12:37.396725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10c1c1cabdb9'
down_revision = '556823bfe3a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('front_user',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('_password', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('realname', sa.String(length=50), nullable=True),
    sa.Column('avatar', sa.String(length=150), nullable=True),
    sa.Column('signatrue', sa.String(length=500), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'SECRET', 'UNKNOW', name='genderenum'), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telephone')
    )
    op.create_foreign_key(None, 'cms_role_user', 'cms_user', ['cms_user_id'], ['id'])
    op.create_foreign_key(None, 'cms_role_user', 'cms_role', ['cms_role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cms_role_user', type_='foreignkey')
    op.drop_constraint(None, 'cms_role_user', type_='foreignkey')
    op.drop_table('front_user')
    # ### end Alembic commands ###
