"""merge feature and dev migrations

Revision ID: 5cceb508aa30
Revises: 55c1a9e0de40, fbf1781f771c
Create Date: 2025-09-01 10:03:54.633474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cceb508aa30'
down_revision: Union[str, Sequence[str], None] = ('55c1a9e0de40', 'fbf1781f771c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
