from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import models, schema
from exceptions import UserNotFoundException, UserAlreadyExistsException

router = APIRouter(prefix="/users", tags=["Users"])


# CREATE USER
@router.post("/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        # Raise custom exception
        raise UserAlreadyExistsException(user.email)

    new_user = models.User(name=user.name, email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET USER BY ID
@router.get("/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        # Raise custom exception
        raise UserNotFoundException(user_id)

    return user