# Read-only endpoint
from fastapi import APIRouter
from ..orm_models.listing import ListingDB
from ..pydantic_schemas.listing import CarListing, ScrapedData
from ..dependencies import get_database_session, Session, Depends

router = APIRouter(prefix="/api", tags=["listings"])

@router.get("/listings", response_model=ScrapedData)
async def get_listings(limit: int = 10, db: Session = Depends(get_database_session)):

    listings = (
        db.query(ListingDB)
        .order_by(ListingDB.timestamp.desc())
        .limit(limit)
        .all()
    )
    return ScrapedData(
        CarListings=[CarListing.model_validate(l) for l in listings]
    )
