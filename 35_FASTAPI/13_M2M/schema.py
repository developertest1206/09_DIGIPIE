from pydantic import BaseModel
from typing import List

# ---------------- COURSE ----------------
class CourseCreate(BaseModel):
    title: str

class CourseOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True



# ---------------- STUDENT ----------------
class StudentCreate(BaseModel):
    name: str

class StudentOut(BaseModel):
    id: int
    name: str
    courses: List[CourseOut] = []

    class Config:
        from_attributes = True

    