# Import tools for token creation, time handling, and password security
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
import models

# This is a built-in form for handling token input (Authorization header)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials     

# Secret key is used to lock and unlock the token (like a password for token)
SECRET_KEY = "mysecretkey"

# Algorithm used to create token (method of encryption)
ALGORITHM = "HS256"


# This is used to convert password into a secure format (hash) and to verify password during login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------- PASSWORD HASH --------

# This function converts normal password into secure unreadable format
def hash_password(password: str):
    return pwd_context.hash(password)

# This function checks if the password entered by user is correct by comparing it with the hashed password stored in database
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)





# -------- ACCESS TOKEN CREATION --------
# This function creates a token (like a login pass)
def create_access_token(data:dict):
    to_encode = data.copy()                              # Copy user data (example: username) into new variable (don't change original data)
    expire = datetime.utcnow() + timedelta(minutes=1)      # Set expiry time (token valid for 1 minutes)
    to_encode.update({"exp" : expire})                   # Add expiry time into data (so we can check it later when user sends token)
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # create token using user data, secret key and algorithm
    return token                               # Return the created token to user (so they can use it in future requests)              


# -------- REFRESH TOKEN CREATION --------
# This function creates a refresh token (like a long-term login pass that can be used to get new access tokens without logging in again)
def create_refresh_token(data: dict):
    to_encode = data.copy()                              # Copy user data (example: username) into new variable (don't change original data)
    expire = datetime.utcnow() + timedelta(days=7)      # Set expiry time (token valid for 7 days)
    to_encode.update({"exp" : expire})                   # Add expiry time into data (so we can check it later when user sends token)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # create token using user data, secret key and algorithm
    return encoded_jwt                               # Return the created token to user (so they can use it in future requests)   


# -------- VERIFY TOKEN --------
# This function checks if token is valid or not (not fake, not expired)
def verify_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)       # Decode token using same secret key and algorithm (if token is fake or expired, it will show error) 
        return payload        # If token is correct, return user data (payload)
    except JWTError as e:
        print("JWT Error:", e)
        return None     # If token is wrong, expired, or fake → return None 
    

# -------- GET CURRENT USER --------
# This line creates a security system that will read token from request header
# It expects data in this format: Authorization: Bearer <token>
security = HTTPBearer()

# -------- GET CURRENT USER --------
# This function is used to check if the user is logged in or not
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials     # Get the actual token value (remove "Bearer" word automatically)
    payload = verify_token(token)       # Check if token is valid (not fake, not expired)

    if payload is None:
        # If token is wrong or expired, stop user and show error
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    # get user from database using email from token payload (payload contains user data like name, email, role, etc..)
    user = db.query(models.User).filter(models.User.email == payload["sub"]).first()

    return user          # If token is correct, return user data from db 