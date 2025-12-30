'''
# PACKAGES
from fastapi import FastAPI, HTTPException # communication endpoints
from pydantic import BaseModel, ConfigDict, field_validator # data validation library (type hints in API response/requests)
from typing import List, Optional # type hints
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker # creates a base class for defining database tables, sessionfactory to interact with database
from datetime import datetime
from celery import Celery # distributed task queue for handling asynchronous database queries and selenium searches
import logging

# import for selenium stuff later
import random

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
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # incase no timestamp is passed
    comparables = Column(String, nullable=True) # store comparable listings as JSON (or later as a separate table)

Base.metadata.create_all(bind=engine)

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

# Pydantic model verifying API requests
class CarListing(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, # converts field names in JSON output to camelCase
        populate_by_name=True, # allows model creation with fields of either original names (snake_case) or alias (camelCase)
        from_attributes=True # allows ORM to pydantic conversion
        )
    
    id: int # will come from frontend temporary ID
    title: str
    price: float
    image_url: str
    mileage: int
    location: str
    timestamp: int # MODIFY SO AUTOMATIC
    comparables: Optional[str] = None

    @field_validator("timestamp", mode="before") # convert timestamp (s) to (ms) when returning JSON response to frontend
    def convert_datetime_to_ms(cls, v):
        if isinstance(v, datetime):
            return int(v.timestamp()*1000)
        return v

    def to_orm(self) -> ListingDB: # Automatically convert pydantic to ORM based on field names
        return ListingDB(
            **self.model_dump(exclude={"timestamp"}),
            timestamp=datetime.fromtimestamp(self.timestamp / 1000) # convert ms received from frontend to s
        )

class ScrapedData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    CarListings: List[CarListing]

class Recommendation(BaseModel):
    id: int
    score: float

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]

# FAST API ENDPOINTS (add await functionality to async functions)------------------------------------
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

# Scrape endpoint (updated to match current models and session setup)
@app.post("/api/scrape", response_model = RecommendationResponse)
async def scrape_data(data: ScrapedData):
    db = local_session()
    try:
        # Store listings in DB
        db_listings = []

        for item in data.CarListings:
            db_listing = item.to_orm()
            db.add(db_listing)
            db_listings.append(db_listing)

        db.commit() # ids are generated here

        # Trigger async comparable searches (placeholder for now)
        for db_listing in db_listings:
            process_comparables.delay(db_listing.id) # must access return value

        # Return immediate recommendations (placeholder for now) may need to change to pydantic automatic conversion (or not if ml based)
        recommendations = [
            {"id": listing.id, "score": 2000 + listing.id * 100}
            for listing in db_listings
        ]

        logger.info(f"Stored {len(db_listings)} listings")
        return RecommendationResponse(recommendations=recommendations)

    except Exception as e:
        db.rollback()
        logger.error(f"Error storing listings: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store listings")

    finally:
        db.close()

# CELERY TASKS ----------------------------
# Celery task for async processing (DEFINE CELERY WORKER WITH REDIS)
@celery.task
def process_comparables(listing_id: int):
    # Fetch the listing from DB
    db = local_session()
    try:
        listing = db.query(ListingDB).filter(ListingDB.id == listing_id).first()
        if not listing:
            logger.error(f"Listing ID {listing_id} not found")
            return {"listing_id": listing_id, "comps": []}
        
        # Compute random modified price (within 2k of the price point)
        original_price = listing.price
        random_offset = max(random.randint(-2000, 2000), 0)
        modified_price = original_price + random_offset
        
    except Exception as e:
        logger.error(f"Error in task for {listing_id}: {str(e)}")
        return {"listing_id": listing_id, "comps": []}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
# New version
from fastapi import FastAPI
from app.routers import listings, scrape
from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(listings.router)
app.include_router(scrape.router)
