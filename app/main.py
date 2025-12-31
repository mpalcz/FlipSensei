from fastapi import FastAPI
from .routers import listings, scrape
from .database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(listings.router)
app.include_router(scrape.router)

@app.get("/")
async def root():
    return {"message": "hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
