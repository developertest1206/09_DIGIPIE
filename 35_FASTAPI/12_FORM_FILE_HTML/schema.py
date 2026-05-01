from pydantic import BaseModel

class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    course: str
    photo: str

    class Config:
        from_attributes= True