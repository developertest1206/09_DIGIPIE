from fastapi import FastAPI, Depends          # Import FastAPI to create the web application (API) and Depeneds to handle dependencies
from sqlalchemy.orm import Session            # Import Session to interact with the database 
import models, schema                              
from db import engine, get_db, Base                # db for database connection and session management and Base for creating tables
from auth import get_current_employee, require_role    # auth for authentication and authorization functions


# This line creates all database tables automatically if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()             # Create FastAPI application instance


# -------------------- CREATE USER --------------------
@app.post("/create-user", response_model=schema.Employee)
def employee_create(employee: schema.EmployeeCreate, db: Session = Depends(get_db)):
    new_user = models.Employee(
        name = employee.name,
        role = employee.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# -------------------- USER GET ONLY --------------------
@app.get("/employee-profile")
def user_data(user = Depends(require_role("employee"))):
    
    # Only normal user can access
    return {
        "message": "Welcome User"
    }

# -------------------- ADMIN GET PROFILE --------------------
@app.get("/admin-profile")
def employee_get_profile(employee = Depends(require_role("admin"))):
    return employee

# -------------------- GET ROLE --------------------
@app.get("/role")
def employee_get_role(user = Depends(get_current_employee)):
    
    # This returns current user role
    return {
        "message": "This is your profile",
        "role": user["role"]
    }