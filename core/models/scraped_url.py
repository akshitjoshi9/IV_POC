import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone


class ScrapedPage(SQLModel, table=True):
    __tablename__ = "scraped_page"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(index=True, unique=True)
    country_id: uuid.UUID = Field(foreign_key="country.id")
    last_scraped_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    country: Optional["CountryMaster"] = Relationship(back_populates="scraped_page")