# Import FastAPI tools
from fastapi import FastAPI, Header, HTTPException

# Import CORS middleware (important for frontend-backend connection)
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Allowed frontend URL (your HTML runs on this port)
origins = ["http://127.0.0.1:5500"]

# Add CORS settings
app.add_middleware(
    CORSMiddleware,

    # Allow only this frontend to access API
    allow_origins=origins,

    # Allow only GET and POST methods
    allow_methods=["GET", "POST"],

    # Allow cookies/auth headers
    allow_credentials=True,

    # Allow these headers from frontend
    allow_headers=["Authorization", "content-Type"],
)


# -------------------- PUBLIC API --------------------
@app.get("/students")
def get_student():

    # This API is open (no token needed)
    return [
        {'id': 1, 'name': 'Drashti'},
        {'id': 2, 'name': 'Zeel'}
    ]


# -------------------- PROTECTED API --------------------
@app.post("/add-student")
def create_student(name: str, authorization: str = Header(None)):

    # Step 1: Check if Authorization header is present
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    # Step 2: Split header into "Bearer" and "token"
    try:
        scheme, token = authorization.split()
    except:
        raise HTTPException(status_code=400, detail="Invalid header format")

    # Step 3: Check token value
    if token != "mytoken123":
        raise HTTPException(status_code=403, detail="Invalid token")

    # Step 4: If token correct, allow action
    return {
        "message": f"Student {name} added successfully"
    }