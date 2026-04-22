from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas
from db import get_db

router = APIRouter(prefix="/employee", tags=["Employee"])


# CREATE EMPLOYEE
@router.post("/create")
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = models.Employee(**emp.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


# UPDATE EMPLOYEE
@router.put("/update/{emp_id}")
def update_employee(emp_id: int, emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    user = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    user.name = emp.name
    user.password = emp.password
    user.email = emp.email

    db.commit()
    return {"message": "Employee updated"}


# DELETE EMPLOYEE
@router.delete("/delete/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(user)
    db.commit()
    return {"message": "Employee deleted"}


# EmloyeeLogin
@router.post("/login")
def create_emloyeelogin(data: schemas.EmloyeeLogin, db: Session = Depends(get_db)):
    user = db.query(models.Employee).filter(
        models.Employee.name == data.name,
        models.Employee.password == data.password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    log = models.EmployeeLogin(name=data.name, password=data.password)
    db.add(log)
    db.commit()
    db.refresh(log)

    formatted_time = log.login_time.strftime("%Y-%m-%d %I:%M %p")

    return {"message": "Login successful"}