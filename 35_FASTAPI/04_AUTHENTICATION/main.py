# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException   # FastAPI for API, HTTPException for errors
from passlib.context import CryptContext     # Used to hash and verify passwords

from db import database, metadata, engine    # Database connection and table setup
from models import employee                  # Employee table
from schemas import Employee, EmployeeLogin, EmployeeUpdate  # Request models

app = FastAPI()     # Create FastAPI instance

# Create table in MySQL if not exists
metadata.create_all(engine)

# Password hashing setup (for security)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------------------
# Event handlers for startup and shutdown to manage database connection
# -----------------------------------------
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# -----------------------------------------
# API endpoints for registration and login
# -----------------------------------------
# Endpoint to get all employees (for testing purposes)
@app.get("/employees")
async def get_employees():
    try:
        query = employee.select()     # Select all records from the employee table
        return await database.fetch_all(query)   # Fetch and return all employee records as a list of dictionaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a specific employee by name (for testing purposes)
@app.get("/employees/{employee_name}")
async def get_employee(employee_name: str):
    try: 
        query = employee.select().where(employee.c.name == employee_name)   # Select employee record where name matches the provided employee_name
        result = await database.fetch_one(query)    # Fetch one record that matches the employee_name

        # If a record is found, return it. Otherwise, raise a 404 error indicating that the employee was not found
        if result:
            return result    # Return the employee record if found
        else:
            raise HTTPException(status_code=404, detail="Employee not found")   # Raise a 404 error if employee is not found
        
    # Catch any exceptions and return a 500 error with the exception message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

@app.post("/register")
async def register(emp: Employee):
    try:
        query = employee.select().where(employee.c.name == emp.username)         # Check if username already exists
        existing_employee = await database.fetch_one(query)                     # Fetch one record that matches the username

        # If username already exists, raise an error
        if existing_employee:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password before storing it in the database for security
        hashed_password = pwd_context.hash(emp.password)            
        query = employee.insert().values(name=emp.username, password=hashed_password)       # Insert new employee record into the database
        
        # Execute the query to insert the new employee and return a success message
        await database.execute(query)
        return {"message": "Employee registered successfully"}
    
    # Catch any exceptions that occur during the registration process and return a 500 error with the exception message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/login")
async def login(emp: EmployeeLogin):
    try:
        # Fetch the employee record from the database based on the provided username to verify the password
        query = employee.select().where(employee.c.name == emp.username)
        existing_employee = await database.fetch_one(query)

        # If username does not exist or password does not match, raise an error. Otherwise, return a success message
        if not existing_employee:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        else:
            if not pwd_context.verify(emp.password, existing_employee["password"]):
                raise HTTPException(status_code=400, detail="Invalid username or password")
            return {"message": "Login successful"}
        
    # Catch any exceptions that occur during the login process and return a 500 error with the exception message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/employees/{employee_name}")
async def update_employee(employee_name: str, emp: EmployeeUpdate):
    try:
        # Fetch the employee record from the database based on the provided name
        query = employee.select().where(employee.c.name == employee_name)
        existing_employee = await database.fetch_one(query)

        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # If a new password is provided, hash it. Otherwise, keep the existing hashed password. Then update the employee record in the database with the new username and hashed password
        if emp.password:
            hashed_password = pwd_context.hash(emp.password)
        else:
            hashed_password = existing_employee["password"]   # Keep existing hashed password if no new password is provided          
        query = employee.update().where(employee.c.name == employee_name).values(name=emp.username, password=hashed_password)       # Update the employee record in the database with the new username and hashed password
        await database.execute(query)

        return {"message": "Employee updated successfully"}

    # Catch any exceptions that occur during the update process and return a 500 error with the exception message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete("/employees/{employee_name}")
async def delete_employee(employee_name: str):
    try:
        # Fetch the employee record from the database based on the provided name
        query = employee.select().where(employee.c.name == employee_name)
        existing_employee = await database.fetch_one(query)

        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # If the employee exists, delete the record from the database and return a success message
        query = employee.delete().where(employee.c.name == employee_name)     # Delete the employee record from the database where name matches the provided employee_name
        await database.execute(query)
        return {"message": "Employee deleted successfully"}

    # Catch any exceptions that occur during the deletion process and return a 500 error with the exception message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))