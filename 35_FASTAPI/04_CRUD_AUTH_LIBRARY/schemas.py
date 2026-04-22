from pydantic import BaseModel

# --------------------Book--------------------
class BookCreate(BaseModel):
    book_name: str
    author_name: str
    launch_date: str

class Book(BaseModel):
    id: int
    book_name: str
    author_name: str
    launch_date: str

    class config():
        orm_mode = True

# --------------------Employee--------------------
class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str

class Employee(BaseModel):
    id: int
    name: str
    email: str

    class config():
        orm_mode = True

# --------------------EmployeeLogin--------------------
class EmloyeeLogin(BaseModel):
    name: str
    password: str

