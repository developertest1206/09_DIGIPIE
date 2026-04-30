# Import tools to define table columns and relationships
from sqlalchemy import Column, Integer, String
from db import Base

# ---------------- USER TABLE ----------------
# This class creates a table named "users" in the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)      # Unique ID for each user (primary key, index for faster queries)
    name = Column(String, nullable=False)                   # Name of the user (can not be empty)
    email = Column(String, unique=True, index=True)         # email (must be unique, index for faster search )
    password = Column(String)                               # Hashed password (stored securely)                        

    role = Column(String, default="user")                   # Role of the user (default "user" = normal user, admin = special access)