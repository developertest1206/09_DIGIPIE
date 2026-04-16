from fastapi import FastAPI         # Import FastAPI framework (used to create APIs)
from pydantic import BaseModel      # Import BaseModel (used for data validation)
from typing import *                # Import all types (like Optional, List, etc.) 

app = FastAPI()     # Create FastAPI app (instance of FastAPI class)

# Create User model (this defines how request body should look)
class User(BaseModel):
    id: int                # User ID (required)
    name: str              # User name (required)
    email: Optional[str] = None  # Email (optional, default = None)
    age: int               # User age (required)

# Create POST API endpoint
@app.post("/users")
def create_user(user: User):        # 'user' parameter will automatically take data from request body and validate it using User model
    return {
        "message": "User created",  # Simple success message
        "data": user                # Return the same user data
    }