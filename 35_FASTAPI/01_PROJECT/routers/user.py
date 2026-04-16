from fastapi import APIRouter, HTTPException            # for creating router and handling errors
from schemas import UserCreate, UserUpdate, UserResponse    # Importing Pydantic models for request validation and response formatting
from services import user_service                       # Importing user service functions for business logic

router = APIRouter()        # create router instance

# CREATE USER
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # user = request body (validated)
    return user_service.create_user_service(user)


# GET ALL USERS
@router.get("/users", response_model=list[UserResponse])
def get_users():
    return user_service.get_all_users_service()


# GET SINGLE USER
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_service.get_user_service(user_id)

    if not user:
        # return error if not found
        raise HTTPException(status_code=404, detail="User not found")

    return user


# UPDATE USER
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):
    user = user_service.update_user_service(user_id, updated_user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = user_service.delete_user_service(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}