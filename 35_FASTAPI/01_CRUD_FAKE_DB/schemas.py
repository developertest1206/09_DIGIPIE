# pydantic models for request validation and response formatting
from pydantic import BaseModel, EmailStr

# Data from client (POST)
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# Response data
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

# Data for update (PUT)
class UserUpdate(BaseModel):
    name: str
    email: EmailStr