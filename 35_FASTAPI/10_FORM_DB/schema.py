from pydantic import BaseModel      # Used to define data structure (like a format/template)
from datetime import datetime       # Used to handle date and time

# This class defines how item data will look when we send response
class Item(BaseModel):
    id : int                        # Unique ID of item
    item_name : str                 # Name of the item (like Laptop, Mobile)
    price : int                     # Price of the item
    created_at : datetime           # Date and time when item was created

    class Config:
        from_attributes = True      # Allows FastAPI to read data directly from database objects