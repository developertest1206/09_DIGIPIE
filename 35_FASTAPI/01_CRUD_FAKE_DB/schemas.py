from pydantic import BaseModel, EmailStr        # Importing BaseModel and EmailStr from Pydantic library

# Data coming from client (POST)
class UserCreate(BaseModel):        
    name: str               # name is a string
    email: EmailStr         # email is a string that must be a valid email address

# Data coming from client (PUT)
class UserUpdate(BaseModel):
    name: str
    email: EmailStr

# Data going back to client (response)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr