import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


class QuestionMaster(SQLModel, table=True):
    __tablename__="questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: Optional[str] = None
    country_id: uuid.UUID = Field(foreign_key="country.id")
    subcategory_id: uuid.UUID = Field(foreign_key="subcategory.id")
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active: bool = True
    subcategory: Optional["SubCategoryMaster"] = Relationship(back_populates="questions")
    country: Optional["CountryMaster"] = Relationship(back_populates="questions")
