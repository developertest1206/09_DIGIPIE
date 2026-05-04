# main.py

# Import FastAPI
from fastapi import FastAPI, HTTPException

# Import config values
import config

# Create FastAPI app using env variable
app = FastAPI(title=config.APP_NAME)


# -------------------- HOME API --------------------
@app.get("/")
def home():
    
    # Show app name from .env
    return {
        "message": "Welcome to app",
        "app_name": config.APP_NAME
    }


# -------------------- SHOW SECRET (JUST FOR LEARNING) --------------------
@app.get("/secret")
def show_secret():
    
    # Show secret key (do NOT do this in real apps)
    return {
        "secret_key": config.SECRET_KEY
    }


# -------------------- ADMIN CHECK --------------------
@app.get("/admin")
def admin_check(email: str):
    
    # Check if given email is admin email from .env
    if email != config.ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Not admin")

    return {
        "message": "Welcome Admin"
    }