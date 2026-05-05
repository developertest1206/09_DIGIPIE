# Import FastAPI tools
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials




# Create FastAPI app
app = FastAPI()


security = HTTPBearer()


# -------------------- DEPENDENCY 1: CHECK TOKEN --------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    token = credentials.credentials

    # Check token value
    if token != "mytoken123":
        raise HTTPException(status_code=403, detail="Invalid token")

    # Return user info (simple example)
    return {"name": "Rahul", "role": "admin"}

# def get_current_user(authorization: str = Header(None)):
    
#     # Check if header exists
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Token missing")

#     # Split header (Bearer token)
#     try:
#         scheme, token = authorization.split()
#     except:
#         raise HTTPException(status_code=400, detail="Invalid header format")

#     # Check token value
#     if token != "mytoken123":
#         raise HTTPException(status_code=403, detail="Invalid token")

#     # Return user info (simple example)
#     return {"name": "Rahul", "role": "admin"}





# -------------------- DEPENDENCY 2: CHECK ROLE --------------------
def check_admin(user = Depends(get_current_user)):
    
    # Check if user role is admin
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return user


# -------------------- PUBLIC API --------------------
@app.get("/students")
def get_students():
    
    return [
        {"id": 1, "name": "Rahul"},
        {"id": 2, "name": "Aman"}
    ]


# -------------------- PROTECTED API (MULTIPLE DEPENDENCIES) --------------------
@app.get("/admin-data")
def admin_data(user = Depends(check_admin)):
    
    # If user passed both checks, API runs
    return {
        "message": "Welcome Admin",
        "user": user
    }