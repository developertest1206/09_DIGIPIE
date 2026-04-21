from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from db import get_db, engine, Base
from models import UserDB   
from schemas import UserCreate, UserResponse


# ------------------------------
# Lifespan (runs on start/stop)
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")

    # Create tables in DB
    Base.metadata.create_all(bind=engine)

    yield

    print("🛑 App shutting down...")

# ------------------------------
# Create FastAPI app
# ------------------------------
# lifespan=lifespan tells FastAPI to use the lifespan function we defined above to manage startup and shutdown events. 
# This allows us to perform any necessary setup (like creating database tables) when the app starts, and cleanup when it stops.
app = FastAPI(lifespan=lifespan)


# ------------------------------
# CREATE USER
# ------------------------------
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    new_user = UserDB(name=user.name, age=user.age)  # create object

    db.add(new_user)     # add to DB
    db.commit()          # save changes
    db.refresh(new_user) # get updated data (id)

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
    
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ------------------------------
# DELETE USER
# ------------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}