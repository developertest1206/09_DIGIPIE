from sqlalchemy import Column, Integer, String      # Import tools to create table and columns
from db import Base       # Base is used to create table

# ------------------------------
# User Table
# ------------------------------
# This class represents a table in database
class User(Base):
    __tablename__ = "users"   # table name in database

    id = Column(Integer, primary_key=True, index=True)     # id column (unique number for each user)
    name = Column(String)    # name column (stores user name)
    age = Column(Integer)    # age column (stores user age)
