# clean FastAPI project with: JWT Authentication, Refresh Token, Password Hashing, CRUD APIs
# SUPER SIMPLE FLOW
# LOGIN
#   ↓
# access + refresh token
#   ↓
# API → use access token 
# access expired 
#   ↓
# /auth/refresh (send refresh token)
#   ↓
# new access token 
#   ↓
# API works again 




from fastapi import FastAPI                        # Import FastAPI to create the web application (API)
from db import Base, engine                        # Import Base to create tables and engine to connect to database
from routers import auth_router, user_router       # Import routes (API endpoints)


# This line creates all database tables automatically if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()             # Create FastAPI application instance

# Include routers
app.include_router(auth_router.router)      # Connect authentication-related APIs (like login, refresh token)
app.include_router(user_router.router)      # Connect user-related APIs (like register, get user)


# Simple test API. When you open http://127.0.0.1:8000/ in browser, it will show this message
@app.get("/")
def home_get():
    return {"message" : "Welcome to FastAPI with JWT Authentication and Refresh Token!"}