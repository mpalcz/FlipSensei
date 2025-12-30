# write heavy endpoint
from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.schemas.listing import ScrapedData
from app.schemas.recommendation import RecommendationResponse
from app.tasks.comparables import process_comparables
from app.utils.logging import logger

router = APIRouter(prefix="/api", tags=["scrape"])

@router.post("/scrape", response_model=RecommendationResponse)
async def scrape_data(data: ScrapedData):
    db = SessionLocal()
    try:
        db_listings = []
        for item in data.CarListings:
            listing = item.to_orm()
            db.add(listing)
            db_listings.append(listing)

        db.commit()

        for listing in db_listings:
            process_comparables.delay(listing.id)

        return RecommendationResponse(
            recommendations=[
                {"id": l.id, "score": 2000 + l.id * 100}
                for l in db_listings
            ]
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to store listings")
    finally:
        db.close()
