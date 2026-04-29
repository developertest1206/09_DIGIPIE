from fastapi import FastAPI, HTTPException                  # FastAPI for creating API endpoints, HTTPException for handling errors
from schemas import UserCreate, UserUpdate, UserResponse    # schemas for request and response models from pydantic
from services import user_service                           #services for business logic (CRUD operations)

app = FastAPI()     # Create the main FastAPI application


# ---------------- CREATE USER ----------------
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user_service(user)

# ---------------- CREATE USER ----------------
# This API is used to create a new user
# It takes user details (like name, email, etc.) and sends them to the service layer to save in database
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user_service(user)


# ---------------- GET ALL USERS ----------------
# This API returns list of all users from database
@app.get("/users", response_model=list[UserResponse])
def get_users():
    return user_service.get_all_users_service()



# ---------------- GET SINGLE USER ----------------
# This API returns details of one user using user_id
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    # Get user from service
    user = user_service.get_user_service(user_id)

    # If user not found, show error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



# ---------------- UPDATE USER ----------------
# This API updates user details using user_id
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):

    # Update user in database
    user = user_service.update_user_service(user_id, updated_user)

    # If user not found, show error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ---------------- DELETE USER ----------------
# This API deletes a user using user_id
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    # Try to delete user
    success = user_service.delete_user_service(user_id)

    # If user not found, show error
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    # If deleted successfully
    return {"message": "User deleted successfully"}