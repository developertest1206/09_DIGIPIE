from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str

class Student(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True