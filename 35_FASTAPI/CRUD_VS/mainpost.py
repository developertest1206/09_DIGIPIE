from fastapi import FastAPI         # FastAPI is used to build APIs easily
from pydantic import BaseModel      # BaseModel helps validate incoming data
from typing import *                # Used for types like Optional, List, etc.

app = FastAPI()     # Create an app instance (this is your main API)

# This class defines what data we expect when creating a user
class User(BaseModel):
    id: int                # Required → User ID (must be integer)
    name: str              # Required → User name (string)
    email: Optional[str] = None  # Optional → Email (default is None if not provided)
    age: int               # Required → User age (integer)
    is_offer: bool = False # Optional → Offer status (default is False)
    password: str = "Don't show this"  # Optional → Password (default value set)

# This class defines what data we will SEND BACK in response
# (notice password is not included → good for security)
class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    age: int
    is_offer: bool = False

# Create POST API endpoint to add user data to our system : http://localhost:8000/users
@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    # FastAPI automatically:
    # 1. Takes JSON data from request body
    # 2. Validates it using User model
    # 3. Converts it into 'user' object

    print(user)  # Print user data in terminal (for testing/debug)

    # Old response example (commented):
    # return {
    #     "message": "User created",
    #     "data": user
    # }

    return user  # Return user data (password will be hidden automatically)