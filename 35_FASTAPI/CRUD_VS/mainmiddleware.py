# ------------------ IMPORTS ------------------
from fastapi import FastAPI, Request   # FastAPI for API, Request to access request data
import time                            # Used to measure time

# ------------------ APP SETUP ------------------
app = FastAPI()   # Create FastAPI app


# ------------------ MIDDLEWARE ------------------
# Middleware runs before and after every request
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    
    start_time = time.time()   # Save start time when request comes

    response = await call_next(request)  
    # Send request to actual API (like / endpoint)

    process_time = time.time() - start_time  
    # Calculate total time taken to process request

    # Print request details and time taken
    print(
        f"Request: {request.method} {request.url} "
        f"- Process time: {process_time:.4f} seconds"
    )

    return response   # Return response back to user


# ------------------ ROUTE ------------------
@app.get("/")
async def root():
    # Simple API response
    return {"message": "Hello World!"}