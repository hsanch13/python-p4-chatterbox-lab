"""add columns

Revision ID: 06aa63aa7aa3
Revises: e30d1de2ff86
Create Date: 2024-11-20 15:08:32.687933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06aa63aa7aa3'
down_revision = 'e30d1de2ff86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('body', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('username', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('messages', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'updated_at')
    op.drop_column('messages', 'created_at')
    op.drop_column('messages', 'username')
    op.drop_column('messages', 'body')
    # ### end Alembic commands ###
