from fastapi import FastAPI         # Import FastAPI to create the web application (API)
from db import Base, engine         # Import Base to create tables and engine to connect to database
import models, schema               # Import models to create tables and schema to define data structure (like forms)
from routers import users, items    # Import routes (API endpoints) for users and items

Base.metadata.create_all(bind=engine)       # This line creates all database tables automatically if they do not exist

app=FastAPI()                               # Create FastAPI application instance

app.include_router(users.router)    # Connect user-related APIs (like register, login)
app.include_router(items.router)    # Connect item-related APIs (like create item, get item)

# Simple test API. When you open http://127.0.0.1:8000/ in browser, it will show this message
@app.get("/")
def home_get():
    return {"message" : "Welcome to FastAPI!"}