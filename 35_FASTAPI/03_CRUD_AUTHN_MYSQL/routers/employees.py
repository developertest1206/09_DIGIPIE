from fastapi import APIRouter, HTTPException, Depends     # Import tools to create API, handle errors, and use database
from sqlalchemy.orm import Session         # Session is used to talk with the database
from passlib.context import CryptContext   # Used to secure (encrypt) passwords for security
from db import get_db                  # Import database connection dependency
import models, schema                  # Import database table and data models

# ------------------ PASSWORD SECURITY ------------------
# This helps to convert password into secret format (not readable)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create a group of APIs for employees
# All APIs will start with /employees
router = APIRouter(prefix="/employees", tags=["Employee"])

# ------------------ GET ALL EMPLOYEES ------------------
# This API returns all employees from database
@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()     # Get all employee records
    return employees                             # Return list of employees


# ------------------ GET EMPLOYEE BY NAME ------------------
# This API finds one employee using name
@router.get("/employees/{employee_name}")
def get_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()    # Search employee by name
    
    if not employee:
        # If not found, show error
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return employee     # Return employee details


# ------------------ REGISTER (CREATE EMPLOYEE) ------------------
# This API creates a new employee account
@router.post("/register")
def register(emp: schema.Employee, db: Session = Depends(get_db)):

    # Check if username already exists
    existing = db.query(models.Employee).filter(models.Employee.name == emp.username).first()

    # If already exists, show error
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(emp.password)      # Convert password into secure format

    # Create new employee object
    new_employee = models.Employee(
        name=emp.username,
        password=hashed_password
    )

    # Save employee in database
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return {"message": "Employee registered successfully"}       # Return success message


# ------------------ LOGIN ------------------
# This API checks username and password
@router.post("/login")
def login(emp: schema.EmployeeLogin, db: Session = Depends(get_db)):

    # Find employee by username
    employee = db.query(models.Employee).filter(models.Employee.name == emp.username).first()

    # If user not found -> show error
    if not employee:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Check if password is correct
    if not pwd_context.verify(emp.password, employee.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": "Login successful"}      # Return success message


# ------------------ UPDATE EMPLOYEE ------------------
# This API updates employee data
@router.put("/employees/{employee_name}")
def update_employee(employee_name: str, emp: schema.EmployeeUpdate, db: Session = Depends(get_db)):

    # Find employee by name
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()

    # If not found show error
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Update name
    employee.name = emp.username

    # If password is given, update it also 
    if emp.password:
        employee.password = pwd_context.hash(emp.password)

    # Save changes
    db.commit()
    db.refresh(employee)

    return {"message": "Employee updated successfully"}





# ------------------ DELETE EMPLOYEE ------------------
# This API deletes employee using name
@router.delete("/employees/{employee_name}")
def delete_employee(employee_name: str, db: Session = Depends(get_db)):

    # Find employee by name
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()

    # If not found show error
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Delete employee 
    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}
