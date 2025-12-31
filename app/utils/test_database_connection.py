# Test the connection to the database
from sqlalchemy import create_engine, text
from ..database import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())  # Should print (1,)
    conn.commit()  # Ensure transaction is committed (required in SQLAlchemy 2.0)