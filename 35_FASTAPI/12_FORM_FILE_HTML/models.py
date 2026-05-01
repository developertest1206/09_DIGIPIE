from sqlalchemy import Column, Integer, String
from db import Base

class Student(Base):
    __tablename__ = "students"

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True)
    age= Column(Integer)
    course = Column(String)
    photo = Column(String)     # store file name (image)

