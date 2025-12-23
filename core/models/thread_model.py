import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Thread(SQLModel, table=True):
    __tablename__ = "thread"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    # Store user_id as a simple integer (no FK constraint)
    name: Optional[str]
    user_id: uuid.UUID = Field(foreign_key="user.id")
    subcategory_id: uuid.UUID = Field(foreign_key="subcategory.id")
    country_id: uuid.UUID = Field(foreign_key="country.id")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active: bool = Field(default=True)
    message: List["Message"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        }
    )
    user: Optional["User"] = Relationship(back_populates="thread")
    subcategory: Optional["SubCategoryMaster"] = Relationship(back_populates="thread")
    country: Optional["CountryMaster"] = Relationship(back_populates="thread")
