from pydantic import BaseModel          

# ------------------------------
# Request (POST / PUT)
# ------------------------------
class UserCreate(BaseModel):
    name: str
    age: int

# ------------------------------
# Response (GET)
# ------------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True