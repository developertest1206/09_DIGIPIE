# Import tools to define table columns and relationships
from sqlalchemy import Column, Integer, String
from db import Base

# ---------------- EMPLOYEE TABLE ----------------
# This class creates a table named "employees" in the database
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)      # Unique ID for each employee (primary key, index for faster queries)
    name = Column(String, nullable=False)                   # Name of the employee (can not be empty)
    
    role = Column(String, default="employee")                   # Role of the employee (default "employee" = normal employee, admin = special access)