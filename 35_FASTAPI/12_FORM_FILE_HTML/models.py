from sqlalchemy import Column, Integer, String
from db import Base

# This class creates "students" table in database
class Student(Base):
    __tablename__ = "students"   # table name in database

    id = Column(Integer, primary_key=True, index=True)  # unique ID
    name = Column(String, index=True)  # student name
    age = Column(Integer)              # student age
    course = Column(String)            # course name
    photo = Column(String)             # photo file name stored as text