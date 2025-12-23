import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import Column, ForeignKey
from conversation.constant import MessageRoleConstants, MessageStatusConstants
from sqlalchemy.dialects.postgresql import UUID


class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="message.id")
    thread_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("thread.id", ondelete="CASCADE"), nullable=False)
        )
    role: MessageRoleConstants = Field(...)
    content: Optional[str]
    sources: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    status: MessageStatusConstants = Field(...)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    parent: Optional["Message"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Message.id"}
    )
    children: List["Message"] = Relationship(back_populates="parent")
    thread: Optional["Thread"] = Relationship(
        back_populates="message",
        sa_relationship_kwargs={
            "passive_deletes": True
        }
    )
    feedback: Optional["Feedback"] = Relationship(
        back_populates="message",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
            "uselist": False
        }
    )