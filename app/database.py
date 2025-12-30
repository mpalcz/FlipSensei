# Contains connection pooling config, alembic migrations hook, db health checks, test db overrides
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql://flip_user:flip_user_password@localhost:5432/FlipSensei_DB"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass