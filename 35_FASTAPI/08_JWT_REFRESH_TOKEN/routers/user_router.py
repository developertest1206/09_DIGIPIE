from fastapi import APIRouter, Depends
from auth import get_current_user              # This function checks user token and gives current logged-in user
import schema                           # Import data format for response 


# All APIs will start with /users and will be tagged as "Users" in documentation (so we can find them easily in docs)
router = APIRouter(prefix="/users", tags=["Users"])


# ------------------------GET PROFILE (PROTECTED API)------------------------
# This API returns profile of logged-in user
@router.get("/profile", response_model=schema.User)
def get_profile(user = Depends(get_current_user)):

    # get_current_user runs first:
    # 1. Takes token from request
    # 2. Verifies it
    # 3. If valid → returns user data

    # Return logged-in user details
    return user