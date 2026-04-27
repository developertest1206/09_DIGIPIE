# -----------------------------------------IMPORTS-----------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import schema, models

# Password hashing:  Used to convert password into secure format and verify
from passlib.context import CryptContext                
# -----------------------------------------PASSWORD HASH SETUP-----------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")       # Setup for password hashing

# Create router
router = APIRouter(prefix="/users", tags=["Users"])

# -----------------------------------------REGISTER USER (POST)-----------------------------------------
@router.post("/register")
def user_register(user: schema.UserCreate, db:Session= Depends(get_db)):
    # Step 1: Check if email already exists
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        # If email already in database → show error
        raise HTTPException(status_code=400, detail="Email already exists")
        
    # Step 2: Convert password into secure format (HASH)  Example: "1234" → "$2b$12$abcxyz..."
    hashed_password = pwd_context.hash(user.password)

    # Step 3: Create new user object
    new_user = models.Users(
        name=user.name,
        email=user.email,
        password=hashed_password        # store hashed password (NOT real password)
    )

    # Step 4: Save data into database
    db.add(new_user)        # add data
    db.commit()             # save permanently
    db.refresh(new_user)    # get updated data (like id)
        
    # Step 5: Send success message
    return new_user
    

# -----------------------------------------LOGIN USER (POST)-----------------------------------------
@router.post("/login")
def user_login(user: schema.UserLogin, db:Session=Depends(get_db)):
    # Step 1: Find user using email
    # db_user = all(id, name, email, password) data fetched from database
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    if not db_user:
        # If email not found
        raise HTTPException(status_code=404, detail="User not found")
        
    # Step 2: Verify password
    # Compare: user input password VS database stored hashed password
    is_password_correct = pwd_context.verify(user.password, db_user.password)

    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Invalid password")

    # Step 3: Login success
    return {"message" : "Login successful"}
    
    
# -----------------------------------------GET USER WITH ALL BOOKS (BY ID)-----------------------------------------
@router.get("/{user_id}", response_model=schema.UserWithBook)
def get_user(user_id:int, db:Session=Depends(get_db)):
    # Step 1: Find user using id
    existing_user = db.query(models.Users).filter(models.Users.id == user_id).first()

    # If user not found → error
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # if exisit user than Return user + their books
    return existing_user

# -----------------------------------------GET ALL USERS (WITH PAGINATION)-----------------------------------------
@router.get("/", response_model=list[schema.UserWithBook])
def get_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Users).offset(skip).limit(limit).all()       # Example: skip=0 → start from beginning; limit=10 → show only 10 users