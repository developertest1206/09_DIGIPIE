from fastapi import FastAPI         # Import FastAPI to create API
from db import Base, engine         # Import database base and engine
from routers import student         # Import router file
import models                       # Import models so tables can be created

# Create all tables in database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Add student routes to app
app.include_router(student.router)

# simple test API
@app.get("/")
def home():
    return {"message": "M2M Student Course API running"}