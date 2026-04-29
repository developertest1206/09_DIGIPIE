# Import required tools to create database table and connect with database
from sqlalchemy import Column, Integer, String
from db import Base

# This class represents a table in the database
class UserDB(Base):
    __tablename__ = "users"   # Table name in database

    id = Column(Integer, primary_key=True, index=True)      # id column (unique number for each user)
    name = Column(String)           # name column (stores user's name)
    age = Column(Integer)           # age column (stores user's age)