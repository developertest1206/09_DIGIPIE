# Import required tools
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# This is a built-in form for handling username/password input
from fastapi.security import OAuth2PasswordRequestForm      

# Import database models and schema (data format)
import models, schema
from db import get_db

# Import password and token functions
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/user", tags=["Users"])          # All APIs will start with /user and will be tagged as "Users" in documentation



# -------- REGISTER --------
# This API is used to create a new user
@router.post("/register")
def user_register(user: schema.UserCreate, db: Session = Depends(get_db)):

    # Step 1: Check if username already exists
    db_user = db.query(models.Users).filter(models.Users.username == user.username).first()
    if db_user:
        # If username already taken → show error
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Step 2: Create new user
    new_user = models.Users(
        username = user.username,
        password = hash_password(user.password)     # Password is converted into secure format (hashed)
    )

    # Step 3: Save user in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Step 4: Return success message
    return {"message" : "User created"}





# -------- LOGIN --------
# This API is used to login user. It takes only username and password (form data)
@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Step 1: Find user using username
    db_user = db.query(models.Users).filter(models.Users.username == form_data.username).first()

    if not db_user:
        # If user not found → show error
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Check password
    # Compare user input password with stored hashed password
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong Password")
    
    # Step 3: Create token (like login pass)
    token = create_token({"sub" : db_user.username})

    # Step 4: Return token to user (they will use this token to access protected APIs)
    return {"access_token": token, "token_type": "bearer"}