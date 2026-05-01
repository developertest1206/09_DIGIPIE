# Import tools to define table columns and data types
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime        # for handling datetime fields
from db import Base                  # to create a model class that inherits


# ---------------- ITEM TABLE ----------------
# This class creates a table named "items" in the database
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)       # Unique ID for each user (primary key, index for faster queries)
    item_name = Column(String, index=True)                   # Name of the item (string, index for faster search)
    price = Column(Integer)                                  # Price of the item(integer)
    created_at = Column(DateTime, default=datetime.now)      # Timestamp for when the item was created (datetime, default to current time)