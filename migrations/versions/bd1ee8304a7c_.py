"""empty message

Revision ID: bd1ee8304a7c
Revises: ed36b8b48b5e
Create Date: 2023-06-29 13:43:04.823085

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bd1ee8304a7c'
down_revision = 'ed36b8b48b5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=postgresql.BYTEA(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('avatar',
               existing_type=postgresql.BYTEA(),
               nullable=False)

    # ### end Alembic commands ###
