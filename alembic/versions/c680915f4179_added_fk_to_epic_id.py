"""added fk to epic_id

Revision ID: c680915f4179
Revises: 39a0eee19515
Create Date: 2025-05-30 21:50:36.375672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c680915f4179'
down_revision: Union[str, None] = '39a0eee19515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'tasks', 'epics', ['epic_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    # ### end Alembic commands ###
