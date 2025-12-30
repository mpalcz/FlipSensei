# PACKAGES
from fastapi import FastAPI, HTTPException # communication endpoints
from pydantic import BaseModel, ConfigDict, field_validator # data validation library (type hints in API response/requests)
from typing import List, Optional # type hints
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase # creates a base class for defining database tables
from sqlalchemy.orm import sessionmaker # to interact with sql database
from datetime import datetime
from celery import Celery # distributed task queue for handling asynchronous database queries and selenium searches
import logging

# import for selenium stuff later

# Create FastAPI application to handle routes and requests
app = FastAPI()

# Set up global logging system (with module specific loggers)
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Database connection set-up (running on local machine)
DATABASE_URL = "postgresql://flip_user:flip_user_password@localhost:5432/FlipSensei_DB"
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Define Listing table schema for ORM
class ListingDB(Base):
    __tablename__ = "CarListings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)
    mileage = Column(Integer)
    location = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    comparables = Column(String, nullable=True) # store comparable listings as JSON (or later as a separate table)

Base.metadata.create_all(bind=engine)

def to_camel(string: str) -> str:
    parts = string.spit('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

# Pydantic model verifying API requests
class CarListing(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True,
        from_attributes=True # allows ORM to pydantic conversion
        )
    
    id: int # will come from frontend temporary ID
    title: str
    price: float
    imate_url: str
    mileage: int
    location: str
    timestamp: int # MODIFY SO AUTOMATIC
    comparables: Optional[str] = None

    @field_validator("timestamp", mode="before")
    def convert_datetime_to_ms(cls, v):
        if isinstance(v, datetime):
            return int(v.timestamp()*1000)
        return v

class ScrapedData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    CarListings: List[CarListing]

# FAST API ENDPOINTS ------------------------------------
@app.get("/")
async def root():
    return {"message": "hello"}

@app.get("/api/listings", response_model = ScrapedData)
async def get_listings(limit: int = 10):
    db = local_session()
    try:
        listings = db.query(ListingDB).order_by(ListingDB.timestamp.desc()).limit(limit).all()
        
        # Convert ORM to Pydantic
        serialized = [CarListing.model_validate(l) for l in listings]

        return ScrapedData(CarListings = serialized)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)