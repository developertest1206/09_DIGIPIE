# Import BaseModel to create data structure (like a form)
from pydantic import BaseModel, EmailStr



# ---------------- USER CREATE ----------------
# This is used when creating a new user (input from user)
class UserCreate(BaseModel):
    name : str    # user enters name
    email : EmailStr   # user enters email 
    password : str   # user enters password
    role: str = "user"   # optional (default user)


# ---------------- USER LOGIN ----------------
# This is used when logging in a user (input from user)
class UserLogin(BaseModel):
    email : EmailStr      # user enters email 
    password : str   # user enters password

# ---------------- USER RESPONSE ----------------
# This is used when showing user data (output)
class User(BaseModel):
    id : int         # user ID from database
    name : str     # name from database
    email : str   # email from database
    role: str    # role from database
    
    class Config:
        orm_mode = True     # This allows us to return SQLAlchemy models directly (instead of converting to dict)


# ---------------- REFRESH TOKEN ----------------
# This is used when user sends refresh token to get new access token (input)
class RefreshToken(BaseModel): 
    refresh_token: str