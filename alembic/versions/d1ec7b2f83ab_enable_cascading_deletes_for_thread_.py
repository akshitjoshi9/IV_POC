"""Enable cascading deletes for Thread -> Message -> Feedback

Revision ID: d1ec7b2f83ab
Revises: 1a9019e5ef9f
Create Date: 2025-08-19 15:44:59.285936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1ec7b2f83ab'
down_revision: Union[str, Sequence[str], None] = '1a9019e5ef9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop old constraints
    op.drop_constraint("message_thread_id_fkey", "message", type_="foreignkey")
    op.drop_constraint("feedback_message_id_fkey", "feedback", type_="foreignkey")

    # Recreate with ON DELETE CASCADE
    op.create_foreign_key(
        "message_thread_id_fkey",
        "message",
        "thread",
        ["thread_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "feedback_message_id_fkey",
        "feedback",
        "message",
        ["message_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Enforce one-to-one: add unique constraint on message_id
    op.create_unique_constraint("uq_feedback_message_id", "feedback", ["message_id"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop new constraints
    op.drop_constraint("uq_feedback_message_id", "feedback", type_="unique")
    op.drop_constraint("feedback_message_id_fkey", "feedback", type_="foreignkey")
    op.drop_constraint("message_thread_id_fkey", "message", type_="foreignkey")

    # Recreate without cascade
    op.create_foreign_key(
        "message_thread_id_fkey",
        "message",
        "thread",
        ["thread_id"],
        ["id"],
    )
    op.create_foreign_key(
        "feedback_message_id_fkey",
        "feedback",
        "message",
        ["message_id"],
        ["id"],
    )
