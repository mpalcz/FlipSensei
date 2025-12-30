from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .utils.logging import logger

def get_database_session():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(str(e))
    finally:
        db.close()