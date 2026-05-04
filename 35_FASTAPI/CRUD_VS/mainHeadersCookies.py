# /login → you get room key
# /profile → show key to enter room
# /logout → return key
# /secure → security guard checks your ID card (token)


# FINAL UNDERSTANDING
# Cookie = automatic (browser handles)
# Header = manual (you send it)
# Login = set cookie
# Profile = read cookie
# Secure API = validate header




from fastapi import FastAPI, Header, Cookie, HTTPException, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



app = FastAPI()


security = HTTPBearer()

# -------------------- LOGIN (SET COOKIE) --------------------
@app.post("/login")
def login(response: Response):

    # This is just demo login (no password check).  In real app, you check email/password

    # Create a simple session id
    session_id = "abc123"

    # Set cookie in browser
    response.set_cookie(
        key="session_id",      # cookie name
        value=session_id,      # cookie value
        httponly=True          # security (JS cannot access)
    )

    return {
        "message": "Login successfully",
        "session_id": session_id
    }

# -------------------- READ COOKIE --------------------
@app.get("/profile")
def get_profile(session_id: str = Cookie(None)):

    # If cookie not found
    if not session_id:
        raise HTTPException(status_code=401, detail = "Not logged in")
    
    # Return user info
    return {
        "message" : "Use Profile",
        "session_id" : session_id
    }

# -------------------- LOGOUT (DELETE COOKIE) --------------------
@app.post("/logout")
def logout(response: Response):

    # Remove cookie from browser
    response.delete_cookie("session_id")

    return {"message" : "Logged out successfully"}

# -------------------- HEADER EXAMPLE --------------------
@app.get("/header-data")
def header_example(token: str = Header(None)):

    # Check if token is present
    if not token:
        return {"message": "No Token Provided"}
    
    return {
        "message": "Header recived",
        "token": token
    }

# -------------------- PROTECTED ROUTE USING HEADER --------------------
@app.get("/secure")
def secure_route(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    if token != "abc123":
        raise HTTPException(status_code=403, detail="Invalid token")

    return {"message": "Access granted"}