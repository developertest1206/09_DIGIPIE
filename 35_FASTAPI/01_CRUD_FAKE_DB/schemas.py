# These models are used to control what data comes in and goes out of API
from pydantic import BaseModel, EmailStr


# -------- CREATE USER (INPUT) --------
# This is the data we expect from user when creating new user
class UserCreate(BaseModel):
    name: str                 # user name
    email: EmailStr           # user email (must be valid email format)


# -------- RESPONSE (OUTPUT) --------
# This is the data we send back to client after processing
class UserResponse(BaseModel):
    id: int                   # user id
    name: str                 # user name
    email: EmailStr           # user email


# -------- UPDATE USER --------
# This is the data used when updating user details
class UserUpdate(BaseModel):
    name: str                 # updated name
    email: EmailStr           # updated email