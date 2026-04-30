# Import BaseModel to create data structure (like a form)
from pydantic import BaseModel



# ---------------- EMPLOYEE CREATE ----------------
# This is used when creating a new employee (input from employee)
class EmployeeCreate(BaseModel):
    name : str    # employee enters name
    role: str = "employee"   # optional (default employee)


# ---------------- EMPLOYEE RESPONSE ----------------
# This is used when showing employee data (output)
class Employee(BaseModel):
    id : int         # employee ID from database
    name : str     # employee from database
    role: str    # role from database
    
    class Config:
        orm_mode = True     # This allows us to return SQLAlchemy models directly (instead of converting to dict)