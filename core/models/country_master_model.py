import uuid
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


class CountryMaster(SQLModel, table=True):
    __tablename__="country"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: Optional[str] = None
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active: bool = True
    category: List["CategoryMaster"] = Relationship(back_populates="country")
    datasource: List["DataSourceMaster"] = Relationship(back_populates="country")
    questions: List["QuestionMaster"] = Relationship(back_populates="country")
    thread: List["Thread"] = Relationship(back_populates="country", sa_relationship=relationship("Thread", back_populates="country"))
    scraped_page: List["ScrapedPage"] = Relationship(back_populates="country")

 
class DataSourceMaster(SQLModel, table=True):
    __tablename__="datasource"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    link: Optional[str] = None
    country_id: uuid.UUID = Field(foreign_key="country.id", nullable=False)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    is_active: bool = True
    country: Optional["CountryMaster"] = Relationship(back_populates="datasource")
