from fastapi import FastAPI, Depends, HTTPException, Header


# -------- GET CURRENT EMPLOYEE --------
# This function gets current employee info from request header (in real life we would use token instead of header for security but this is just a simple example)
def get_current_employee(role: str = Header(...)):
    
    # In real life, we would decode the token to get employee info and role, but here we just take role from header for simplicity 
    return {"role": role}
     


# -------- REQUIRE ROLE --------
# This function checks if employee has required role
def require_role(required_role: str):

    # This inner function will run when API is called
    def checker(employee = Depends(get_current_employee)):

        # If role does not match → deny access
        if employee["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to access this"
            )

        # If role matches → allow access
        return employee

    return checker