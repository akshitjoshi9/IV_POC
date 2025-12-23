import uuid

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, List
from datetime import datetime, timezone
from conversation.constant import FeedbackReactionsConstants


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    message_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("message.id", ondelete="CASCADE"), nullable=False)
    )
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    reactions: Optional[FeedbackReactionsConstants] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active: bool = True
    message: Optional["Message"] = Relationship(
        back_populates="feedback",
        sa_relationship_kwargs={
            "passive_deletes": True
        }
    )
    user: List["User"] = Relationship(back_populates="feedback")
