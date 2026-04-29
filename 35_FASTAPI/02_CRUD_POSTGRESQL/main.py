# Import FastAPI to create APIs, Depends for dependency injection, HTTPException for error handling 
from fastapi import FastAPI, Depends, HTTPException      
from sqlalchemy.orm import Session            # Session is used to talk with database
from contextlib import asynccontextmanager    # Used to run code when app starts and stops

from db import get_db, engine, Base       # Import database connection and table base class 
import models, schemas                    # import our database models and pydantic schemas


# ------------------------------
# Lifespan (runs when app starts and stops)
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")
    Base.metadata.create_all(bind=engine)   # Create database tables if not already created
    yield   # App runs here
    print("App shutting down...")



# ------------------------------
# Create FastAPI app
# ------------------------------
# lifespan=lifespan tells FastAPI to use the lifespan function we defined above to manage startup and shutdown events. 
# This allows us to perform any necessary setup (like creating database tables) when the app starts, and cleanup when it stops.
app = FastAPI(lifespan=lifespan)


# ------------------------------
# CREATE USER
# ------------------------------
# This API creates a new user in database
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.User(name=user.name, age=user.age)        # Create new user object using input data

    db.add(new_user)    # Add user to database
    db.commit()          # Save changes to database
    db.refresh(new_user)    # Refresh to get updated data (like auto id)

    return new_user    # Return created user


# ------------------------------
# GET ALL USERS
# ------------------------------
# This API returns all users from database
@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()  # Query all users from database and return as list


# ------------------------------
# GET USER BY ID
# ------------------------------
# This API returns one user using user id
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    # Find user by id in database
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # If user not found, show error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  


# ------------------------------
# DELETE USER
# ------------------------------
# This API deletes a user using user id
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    # Find user by id in database
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # If not found, show error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    db.delete(user)    # Delete user from database
    db.commit()    # Save changes

    return {"message": "User deleted successfully"}