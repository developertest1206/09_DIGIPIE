from fastapi import FastAPI, Request
from db import engine, Base     # Import database connection and Base (used to create tables)
from routers import users, books        # Import all API routes (user and book APIs)
import time             # Import time module (used to measure request time)

# This will create tables in database automatically (if not already created)
Base.metadata.create_all(bind=engine)

# Create main FastAPI application
app = FastAPI()

# Add user and book APIs into main app
app.include_router(users.router)
app.include_router(books.router)

# Something that runs before and after every request
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()        # Start timer when request comes
    response = await call_next(request)     # Process the request (run actual API)
    process_time = time.time() - start_time     # Calculate how much time it took
    print(f"URL: {request.url} | Time: {process_time}")     # Print in terminal: URL: http://127.0.0.1:8000/books | Time: 0.02    
    return response

# This is a simple test API
@app.get("/")
def home_get():
    return {"message" : "Library Management API Running..."}