# PACKAGES
from fastapi import FastAPI, HTTPException # communication endpoints
from pydantic import BaseModel # data validation library (type hints in API response/requests)
from typing import List # type hints
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase # creates a base class for defining database tables
from sqlalchemy.orm import sessionmaker # to interact with sql database
from datetime import datetime
from celery import Celery # distributed task queue for handling asynchronous tasks
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
    comparables = Column(String, nullable=True) # store comparable listings as JSON

Base.metadata.create_all(bind=engine)

# Pydantic model verifying API
class CarListing(BaseModel):
    id: int # will come from frontend temporary ID
    title: str
    price: float
    imageUrl: str
    mileage: int
    location: str
    timestamp: int

# confligure camelCase -> snake_case!!!!!!!!!!!!!!!

class ScrapedData(BaseModel):
    CarListings: List[CarListing]