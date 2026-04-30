# Import tools to define table columns and relationships
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# ---------------- USER TABLE ----------------
# This class creates a table named "users" in the database
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)      # Unique ID for each user (primary key, index for faster queries)
    username = Column(String, unique=True)                  # Username (must be unique)
    password = Column(String)                               # Hashed password (stored securely)                        

    items = relationship("Items", back_populates="user")    # Relationship to access user's items (and vice versa)

# ---------------- ITEM TABLE ----------------
# This class creates a table named "items" in the databaseclass Items(Base):
class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)      # Unique ID for each item (primary key, index for faster queries)
    title = Column(String)                                  # Title of the item

    owner_id = Column(Integer, ForeignKey("users.id"))      # Foreign key linking to users table (owner of the item)
    user = relationship("Users", back_populates="items")    # Relationship to access owner details from item (and vice versa)