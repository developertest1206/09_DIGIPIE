from sqlalchemy import Column, Integer, String        # Import tools to create table and columns
from db import Base                    # Base is used to create table

# --------------------------Employee Table---------------------------
# This class represents a table in database
class Employee(Base):
    __tablename__ = "employees"        # table name in database

    id = Column(Integer, primary_key=True, index=True)       # id column (unique number for each user)
    name = Column(String(50), unique=True, nullable=False)   # name column (stores employee naem and must be unique and not empty)
    password = Column(String(255), nullable=False)           # password column (stores user password and must not be empty)