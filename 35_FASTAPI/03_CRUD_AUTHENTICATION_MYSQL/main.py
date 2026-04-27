# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException, Depends     # FastAPI for API, HTTPException for errors
from db import engine, Base         # Database connection and table setup
from routers import employees

# ------------------ APP ------------------
app = FastAPI()     # Create FastAPI instance

app.include_router(employees.router)

# ------------------ CREATE TABLE ------------------
# This will create table in MySQL if it doesn't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def home_get():
    return {"message" : "Library Management API Running..."}