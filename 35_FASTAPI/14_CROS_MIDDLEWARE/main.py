from fastapi import FastAPI
# Import the FastAPI tool, which helps you create a web server (API)

from fastapi.middleware.cors import CORSMiddleware
# Import CORS middleware, which controls who is allowed to talk to your server

# Create a new FastAPI application (your backend server)
app = FastAPI()


# List of allowed frontend origins
origins = [
    "http://127.0.0.1:5500"         # This means: only this live server website (your frontend) is allowed to call this API
]


# Add middleware to app
app.add_middleware(
    CORSMiddleware,            # Attach CORS rules to your app
    allow_origins=origins,     # Only allow requests coming from the origins listed above
    allow_credentials=True,    # Allow sending cookies or login information along with requests
    allow_methods=["GET"],     # Allow all types of requests like GET, POST, PUT, DELETE
    allow_headers=["*"],       # Allow all kinds of headers (extra information sent with requests)
)


# -------------------- SIMPLE API --------------------
# This means: when someone opens the main URL (like http://127.0.0.1:8000/) this function will run
@app.get("/data")
def get_data():
    
    # This API returns simple data in JSON Format
    return {
        "message": "Hello from FastAPI"
    }