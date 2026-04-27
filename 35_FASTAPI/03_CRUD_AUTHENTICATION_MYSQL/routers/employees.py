from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db import get_db
import models, schema

# ------------------ PASSWORD SECURITY ------------------
# This is used to encrypt (hide) passwords (for security)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/employees", tags=["Employee"])

# ✅ GET ALL EMPLOYEES
@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    return employees


# ✅ GET EMPLOYEE BY NAME
@router.get("/employees/{employee_name}")
def get_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# ✅ REGISTER (CREATE USER)
@router.post("/register")
def register(emp: schema.Employee, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(models.Employee).filter(models.Employee.name == emp.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Hash password (secure)
    hashed_password = pwd_context.hash(emp.password)

    # Create new employee object
    new_employee = models.Employee(
        name=emp.username,
        password=hashed_password
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"message": "Employee registered successfully"}


# ✅ LOGIN
@router.post("/login")
def login(emp: schema.EmployeeLogin, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == emp.username).first()
    if not employee:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Check password
    if not pwd_context.verify(emp.password, employee.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}


# ✅ UPDATE EMPLOYEE
@router.put("/employees/{employee_name}")
def update_employee(employee_name: str, emp: schema.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Update name
    employee.name = emp.username

    # Update password (if given)
    if emp.password:
        employee.password = pwd_context.hash(emp.password)
    db.commit()
    db.refresh(employee)
    return {"message": "Employee updated successfully"}


# ✅ DELETE EMPLOYEE
@router.delete("/employees/{employee_name}")
def delete_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == employee_name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
