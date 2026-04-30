from fastapi import FastAPI, Form       # FastAPI to create API and Forn to handle form data
from typing import Optional             # Optional is used to indicate that a parameter is optional (not required)

app = FastAPI()    # Create an instance of FastAPI

# -------------------- HOME ROUTE --------------------
# This is just to check server is running
@app.get("/")  
def home():
    return {"message" : "Welcome to the FastAPI Form Data Handling Example!"}

# -------------------- LOGIN FORM --------------------
# This API will accept form data (not JSON)
@app.post("/login")
# The parameters of the function are defined name and password with form(...) to indicate they are expected as form data in the form input.
# The (...) Ellipsis is used to indicate that these fields are required
def login(name: str = Form(...), password: str=Form(...)):

    print("Name :", name, "Password :", password)          # Print values in terminal (for understanding)

    # Here we just return data (no database for now)
    return {
        "message" : f"Hello {name}, you have successfully LOGGED IN!"
    }

# -------------------- REGISTER FORM --------------------
# This API accepts multiple form fields
@app.post("/register")
# # The parameters of the function are defined name, email and password with Form(...), Form(None) to indicate they are expected as form data in the form input.
# The (...) Ellipsis is used to indicate that these fields are required and (None) is used to indicate that the email field is optional (not required)
def register(name: str =Form(...), email:  Optional[str] = Form(None), password: str = Form(...)):

    print("Name :", name, "Email :", email, "Password :", password)                  # Print values in terminal (for understanding)

    # Here we just return data (no database for now)
    return {
        "message" : "User registered successfully!",
        "name" : name,
        "password" : password,
        "email" : email
    }   