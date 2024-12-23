"""Create trigger on students table

Revision ID: 1af43302ec33
Revises: a6f351b72735
Create Date: 2024-12-23 17:40:16.567992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1af43302ec33'
down_revision: Union[str, None] = 'a6f351b72735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
