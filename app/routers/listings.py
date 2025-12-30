# Read-only endpoint
from fastapi import APIRouter
from app.database import SessionLocal
from app.models.listing import ListingDB
from app.schemas.listing import CarListing, ScrapedData

router = APIRouter(prefix="/api", tags=["listings"])

@router.get("/listings", response_model=ScrapedData)
async def get_listings(limit: int = 10):
    db = SessionLocal()
    try:
        listings = (
            db.query(ListingDB)
            .order_by(ListingDB.timestamp.desc())
            .limit(limit)
            .all()
        )
        return ScrapedData(
            CarListings=[CarListing.model_validate(l) for l in listings]
        )
    finally:
        db.close()
