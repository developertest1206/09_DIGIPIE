# Import BaseModel to create data structure (like a form)
from pydantic import BaseModel
from typing import List

# ---------------- USER CREATE ----------------
# This is used when creating a new user (input from user)
class UserCreate(BaseModel):
    username : str   # user enters username
    password : str   # user enters password

# ---------------- USER RESPONSE ----------------
# This is used when showing user data (output)
class User(BaseModel):
    id : int         # user ID from database
    username : str   # username from database
    
    class Config:
        orm_mode = True     # This allows us to return SQLAlchemy models directly (instead of converting to dict)





# ---------------- ITEM CREATE ----------------
# This is used when creating a new item
class ItemCreate(BaseModel):
    title : str      # user enters item name

# ---------------- ITEM RESPONSE ----------------
# This is used when showing item data
class Item(BaseModel):
    id : int         # item ID from database
    title : str      # item name

    class Config:
        orm_mode = True   # allows data to come from database models