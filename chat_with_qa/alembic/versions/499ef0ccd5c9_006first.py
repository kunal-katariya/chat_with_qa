"""006first

Revision ID: 499ef0ccd5c9
Revises: da9b62c95805
Create Date: 2024-01-16 17:14:45.396081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '499ef0ccd5c9'
down_revision: Union[str, None] = 'da9b62c95805'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unanswered_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_question', sa.String(length=30), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_resolved', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('is_resolved'),
    sa.UniqueConstraint('user_question')
    )
    op.create_unique_constraint(None, 'conversation', ['id'])
    op.create_unique_constraint(None, 'intent', ['id'])
    op.alter_column('user', 'user_type',
               existing_type=postgresql.ENUM('admin', 'normal_user', name='role'),
               nullable=True)
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'user_type',
               existing_type=postgresql.ENUM('admin', 'normal_user', name='role'),
               nullable=False)
    op.drop_constraint(None, 'intent', type_='unique')
    op.drop_constraint(None, 'conversation', type_='unique')
    op.drop_table('unanswered_question')
    # ### end Alembic commands ###
