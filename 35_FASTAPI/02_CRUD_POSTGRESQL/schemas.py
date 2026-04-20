# Pydantic is a data validation and settings management library that uses Python type annotations. It allows us to define data models with type hints, and it will automatically validate 
# and serialize/deserialize data based on those models. In this code, we are using Pydantic to define our request and response models for a FastAPI application.
from pydantic import BaseModel          

# ------------------------------
# Request Model
# ------------------------------
class UserCreate(BaseModel):
    name : str
    age : int

# ------------------------------
# Response Model
# ------------------------------
class UserResponse(BaseModel):
    id : int
    name : str
    age : int

    class Config:
        orm_model = True    # This tells Pydantic to read data even if it is not a dict, but an ORM model (like SQLAlchemy model). 
        # This allows us to return SQLAlchemy models directly from our API endpoints and have them automatically converted to the appropriate response format.

