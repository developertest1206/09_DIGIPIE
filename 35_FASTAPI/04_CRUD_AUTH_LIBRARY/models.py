from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base
import datetime

# --------------------Book Table--------------------
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String)
    author_name = Column(String)
    launch_date = Column(String)

# --------------------Employee Table--------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

# --------------------Employee Login Table--------------------
class EmployeeLogin(Base):
    __tablename__ = "employee_login"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    login_time = Column(DateTime(timezone=True), server_default=func.now())