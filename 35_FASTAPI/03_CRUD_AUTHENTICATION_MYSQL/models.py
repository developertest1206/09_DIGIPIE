from sqlalchemy import Column, Integer, String
from db import Base

# Create table "employees"
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)