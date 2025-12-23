import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


class SubCategoryMaster(SQLModel, table=True):
    __tablename__="subcategory"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: Optional[str] = None
    category_id: uuid.UUID = Field(foreign_key="category.id")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active: bool = True
    category: Optional["CategoryMaster"] = Relationship(back_populates="subcategory")
    thread: List["Thread"] = Relationship(back_populates="subcategory")
    questions: List["QuestionMaster"] = Relationship(back_populates="subcategory")
