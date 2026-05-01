from fastapi import APIRouter, Form, HTTPException, Depends   # FastAPI tools to create API and handle form + errors
from sqlalchemy.orm import Session                            # Used to interact with database
from db import get_db                                         # Function to get database connection
import models, schema                                         # Import database models and schema
from datetime import datetime                                 # Used to get current date and time

# Create a group (router) for all item-related APIs
router = APIRouter(prefix="/Items", tags=["Items"])



# -------------------------- CREATE ITEM API --------------------------
@router.post("/create", response_model=schema.Item)
def create_item(
        item_name: str = Form(..., description = "Name of the item",  examples=["Laptop", "Mobile"]),    # Form(...) means data will come from form input (user input). item_name is required (because of ...)
        price: int = Form(..., description = "Price of the item", examples=[1000, 500]),           # price is also required and comes from form
        db: Session = Depends(get_db)                  # This gives database connection automatically
    ):

    # Create a new item object (like creating a new record)
    new_item = models.Item(
        item_name = item_name,           # Set item name from user input
        price = price,                   # Set price from user input
        created_at = datetime.now()      # Save current date and time
    )

    db.add(new_item)          # Add item to database (not saved yet)
    db.commit()               # Save data permanently in database
    db.refresh(new_item)      # Get updated data (like auto ID)

    return new_item      # Return created item as response



# -------------------------- GET ALL ITEMS --------------------------
@router.get("/all_items", response_model=list[schema.Item])
def get_all_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()       # Get all items from database and return


# -------------------------- SEARCH ITEM BY NAME --------------------------
@router.get("/get/{item_name}", response_model=schema.Item)
def search_item(item_name: str, db: Session = Depends(get_db)):

    # Search item in database using item name
    item = db.query(models.Item).filter(models.Item.item_name == item_name).first()

     # If item not found, show error
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item    # Return found item

