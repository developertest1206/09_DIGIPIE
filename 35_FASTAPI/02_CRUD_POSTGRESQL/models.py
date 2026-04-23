# Column is a class that defines a column in a database table, Integer and String are data types for the columns
from sqlalchemy import Column, Integer, String
from db import Base 

# ------------------------------
# User Table
# ------------------------------
class User(Base):
    __tablename__ = "users"   # table name

    id = Column(Integer, primary_key=True, index=True)  # unique id
    name = Column(String)     # user name
    age = Column(Integer)     # user age
