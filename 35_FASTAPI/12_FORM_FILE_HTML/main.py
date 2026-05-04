from fastapi import FastAPI
import models, schema
from db import Base, engine
from routers import student

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Connect student routes (APIs) to main app
app.include_router(student.router)

