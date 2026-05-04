from pydantic import BaseModel


# This is used to control what data API returns
class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    course: str
    photo: str

    class Config:
        from_attributes= True