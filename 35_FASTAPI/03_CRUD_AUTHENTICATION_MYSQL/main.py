# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException, Depends     # FastAPI for API, HTTPException for errors
from sqlalchemy.orm import Session
from passlib.context import CryptContext                # Used to hash and verify passwords

from db import engine, Base, get_db   # Database connection and table setup
from models import Employee           # Employee table
from schemas import Employee as EmployeeSchema, EmployeeLogin, EmployeeUpdate   # Request models

# ------------------ APP ------------------
app = FastAPI()     # Create FastAPI instance

# ------------------ CREATE TABLE ------------------
# This will create table in MySQL if it doesn't exist
Base.metadata.create_all(bind=engine)

# ------------------ PASSWORD SECURITY ------------------
# This is used to encrypt (hide) passwords (for security)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================================================
# ===================== ROUTES =============================
# =========================================================

# ✅ GET ALL EMPLOYEES
@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees


# ✅ GET EMPLOYEE BY NAME
@app.get("/employees/{employee_name}")
def get_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == employee_name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# ✅ REGISTER (CREATE USER)
@app.post("/register")
def register(emp: EmployeeSchema, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(Employee).filter(Employee.name == emp.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Hash password (secure)
    hashed_password = pwd_context.hash(emp.password)

    # Create new employee object
    new_employee = Employee(
        name=emp.username,
        password=hashed_password
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"message": "Employee registered successfully"}


# ✅ LOGIN
@app.post("/login")
def login(emp: EmployeeLogin, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == emp.username).first()
    if not employee:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Check password
    if not pwd_context.verify(emp.password, employee.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}


# ✅ UPDATE EMPLOYEE
@app.put("/employees/{employee_name}")
def update_employee(employee_name: str, emp: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == employee_name).first()
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
@app.delete("/employees/{employee_name}")
def delete_employee(employee_name: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == employee_name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
