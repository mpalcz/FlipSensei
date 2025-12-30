# Contains ORM tables, relationships, indexes, constraints etc
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from ..database import Base

class ListingDB(Base):
    __tablename__ = "CarListings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)
    mileage = Column(Integer)
    location = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    comparables = Column(String, nullable=True)
