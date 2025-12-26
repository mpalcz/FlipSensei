# Packages
from fastapi import FastAPI, HTTPException # communication endpoints
from pydantic import BaseModel # data validation library (type hints in API response/requests)
from typing import List # type hints
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base # creates a base class for defining database tables
from sqlalchemy.orm import sessionmaker # to interact with sql database
from datetime import datetime
from celery import Celery # distributed task queue for handling asynchronous tasks
import logging

# import for selenium stuff later

# Create FastAPI application to handle routes and requests
app = FastAPI()

# Set up global logging system
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Database connection set-up
DATABASE_URL = "postgresql://flip_user_password@localhost:5432/FlipSensei_DB"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()