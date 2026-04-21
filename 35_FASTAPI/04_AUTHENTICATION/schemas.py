from pydantic import BaseModel

# Used when creating new employee
class Employee(BaseModel):
    username: str   # input username
    password: str   # input password


# Used when login
class EmployeeLogin(BaseModel):
    username: str
    password: str

# Used when updating employee information
class EmployeeUpdate(BaseModel):
    username: str = None   # Optional new username
    password: str = None   # Optional new password