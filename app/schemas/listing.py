# Contains API data contracts (input/output), validation rules, versioned schemas, public vs internal
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from app.models.listing import ListingDB

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class CarListing(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

    id: int
    title: str
    price: float
    image_url: str
    mileage: int
    location: str
    timestamp: int
    comparables: Optional[str] = None

    @field_validator("timestamp", mode="before")
    def convert_datetime_to_ms(cls, v):
        if isinstance(v, datetime):
            return int(v.timestamp() * 1000)
        return v

    def to_orm(self) -> ListingDB:
        return ListingDB(
            **self.model_dump(exclude={"timestamp"}),
            timestamp=datetime.fromtimestamp(self.timestamp / 1000)
        )

class ScrapedData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    CarListings: List[CarListing]
