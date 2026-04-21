from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from db import get_db, engine, Base
from models import UserDB
from schemas import UserCreate, UserResponse

# ------------------------------
# Lifespan (Modern FastAPI)
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")

    # Create tables (only if not exist)
    Base.metadata.create_all(bind=engine)

    yield

    print("🛑 App shutting down...")

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(lifespan=lifespan)


# ------------------------------
# CREATE USER
# ------------------------------
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # create DB object
    new_user = UserDB(name=user.name, age=user.age)

    # add to DB
    db.add(new_user)

    # save changes
    db.commit()

    # refresh to get ID
    db.refresh(new_user)

    return new_user


# ------------------------------
# GET ALL USERS
# ------------------------------
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()


# ------------------------------
# GET USER BY ID
# ------------------------------
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserDB).filter(UserDB.id == user_id).first()


# ------------------------------
# DELETE USER
# ------------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if not user:
        return {"error": "User not found"}

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}