# Column is a class that defines a column in a database table, Integer and String are data types for the columns
from sqlalchemy import *
from database import Base   # Base is the base class for all models, which we imported from database.py

# ------------------------------
# Create User Table
# ------------------------------
class UserDB(Base):
    __tablename__ = "02_users"      # table name in DB
    id = Column(Integer, primary_key=True, index=True)  # id is an integer column that serves as the primary key and is indexed for faster queries
    name = Column(String) # name is a string column that will store the user's name
    age = Column(Integer) # age is an integer column that will store the user's age

