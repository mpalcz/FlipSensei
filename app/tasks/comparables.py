# background processing
import random
from app.database import SessionLocal
from app.models.listing import ListingDB
from app.celery_worker import celery
from app.utils.logging import logger

@celery.task
def process_comparables(listing_id: int):
    db = SessionLocal()
    try:
        listing = db.query(ListingDB).filter_by(id=listing_id).first()
        if not listing:
            logger.error(f"Listing {listing_id} not found")
            return

        modified_price = listing.price + max(random.randint(-2000, 2000), 0)
        # Selenium logic goes here

    except Exception as e:
        logger.error(str(e))
    finally:
        db.close()
