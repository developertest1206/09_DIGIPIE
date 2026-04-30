from fastapi import APIRouter, Depends, HTTPException     # Import tools for API, database, and error handling
from sqlalchemy.orm import Session         # Import database Session for database operations

import models, schema          # Import database models and data schema
from db import get_db          # Import database connection function
from auth import create_access_token, create_refresh_token, verify_token, hash_password, verify_password    # Import authentication functions

# All APIs will start with /auth and will be tagged as "auth" in documentation (so we can find them easily in docs)
router = APIRouter(prefix="/auth", tags=["auth"])



# ------------------------REGISTER------------------------
# This API creates a new user account and returns the created user data
@router.post("/register", response_model=schema.User)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Create new user object 
    new_user = models.User(
        name=user.name,
        email=user.email, 
        password=hash_password(user.password),     # Password is converted into secure format before saving
        role=user.role                # Save user role (like admin or normal user)
    )

    # Save user into database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user       # Return created user details


# ------------------------LOGIN------------------------
# This API checks user email and password, and if correct -> returns access token and refresh token 
@router.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    # Find user in database using email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    # If user not found or password is wrong -> show error
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    # Create access token (short time login) and refresh token (long time login)
    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})
    refresh_token = create_refresh_token({"sub": db_user.email})

    # Return both tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ------------------------REFRESH TOKEN API------------------------
# This API gives new access token using refresh token 
@router.post("/refresh")
def refresh_token(data: schema.RefreshToken):

    # Verify refresh token 
    payload = verify_token(data.refresh_token)

    # If token is invalid or expired -> show error
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Create new access token using data from refresh token
    new_access_token = create_access_token({
        "sub": payload["sub"],                 # user email from refresh token
        "role": payload.get("role", "user")    # default role = user 
    })

    # Return new access token
    return {"access_token": new_access_token}