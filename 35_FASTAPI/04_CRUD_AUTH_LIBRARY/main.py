from fastapi import FastAPI
from db import Base, engine
from routers import employees, books

app = FastAPI()

Base.metadata.create_all(bind=engine)

# include routers
app.include_router(employees.router)
app.include_router(books.router)

@app.get("/")
def home():
    return {"message": "Library API Running"}