"""last_db

Revision ID: eac7592e4cbd
Revises: 50e46ddfbf3a
Create Date: 2024-02-01 13:03:02.498862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac7592e4cbd'
down_revision: Union[str, None] = '50e46ddfbf3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unanswered_question_user_id_fkey', 'unanswered_question', type_='foreignkey')
    op.create_foreign_key(None, 'unanswered_question', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unanswered_question', type_='foreignkey')
    op.create_foreign_key('unanswered_question_user_id_fkey', 'unanswered_question', 'intent', ['user_id'], ['id'])
    # ### end Alembic commands ###