# BaseModel is used to define data structure
from pydantic import BaseModel          

# ------------------------------
# Request (data coming from user)
# ------------------------------
# This is used when creating or updating user
class UserCreate(BaseModel):
    name: str   # user name
    age: int    # user age


# ------------------------------
# Response (data going to user)
# ------------------------------
# This is what API sends back
class UserResponse(BaseModel):
    id: int     # user id
    name: str   # user name
    age: int    # user age

    class Config:
        orm_mode = True   # Allows reading data from database object