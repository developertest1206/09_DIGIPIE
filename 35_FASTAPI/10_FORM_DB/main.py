from fastapi import FastAPI                # Import FastAPI to create the web application (API)
from db import Base, engine                # Import Base to create tables and engine to connect to database
from routers import item                   # Import routes (API endpoints)

# This line creates all database tables automatically if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()         # Create FastAPI application instance

app.include_router(item.router)     # Include routers

# Simple test API. When you open http://127.0.0.1:8000/ in browser, it will show this message
@app.get("/")
def home():
    return {"message": "Form + Database working"}