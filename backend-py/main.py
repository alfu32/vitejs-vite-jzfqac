from fastapi import FastAPI
from database import Base, engine
from routers import articles, photos

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(articles.router)
app.include_router(photos.router)
