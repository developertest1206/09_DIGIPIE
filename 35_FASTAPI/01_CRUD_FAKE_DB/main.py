from fastapi import FastAPI, HTTPException      
from schemas import UserCreate, UserUpdate, UserResponse
from services import user_service

app = FastAPI()


# CREATE USER
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user_service(user)


# GET ALL USERS
@app.get("/users", response_model=list[UserResponse])
def get_users():
    return user_service.get_all_users_service()


# GET SINGLE USER
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_service.get_user_service(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# UPDATE USER
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):
    user = user_service.update_user_service(user_id, updated_user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = user_service.delete_user_service(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}