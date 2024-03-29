"""Add task ownership

Revision ID: 84e9e3a8dce1
Revises: c97e0c2494b9
Create Date: 2024-03-25 20:26:59.543526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84e9e3a8dce1'
down_revision: Union[str, None] = 'c97e0c2494b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('owner_id', sa.Integer(), nullable=False, default =1))
    op.create_foreign_key(None, 'tasks', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'owner_id')
    # ### end Alembic commands ###
