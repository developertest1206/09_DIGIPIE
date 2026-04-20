from fastapi import FastAPI         # Import FastAPI framework (used to create APIs)
from pydantic import BaseModel      # Import BaseModel (used for data validation)

app = FastAPI()     # Create FastAPI app (instance of FastAPI class)

class User(BaseModel):      # Define User model (structure of user data)
    id: int        # User ID (must be integer)
    name: str      # User name (string)
    age: int       # User age (integer) 

users = []      # Create empty list to store users (acts like a database)

# ------------------------------
# POST - Create new user
# ------------------------------
@app.post("/users")
def create_user(user : User):           # Check if user with same ID already exists
    for u in users:                     # Loop through existing users to check if user with same ID already exists
        if u.id == user.id:             # If ID matches, return error message (ID must be unique for each user)
            return {"error" : "User with this ID already exists. Please use a different ID."}       # Check if user with same ID already exists, if yes return error message
    users.append(user)              # Add user to list (database)
    return {        
        "message" : "User Created",
        "data" : user                  # Return the same user data in response
    }

# ------------------------------
# GET - Get all users
# ------------------------------
@app.get("/users")
def get_users():
    return [user for user in users]             # Return list of all users (using list comprehension to create a new list of user data)

# ------------------------------
# GET - Get user by ID
# ------------------------------
@app.get("/users/{user_id}")            
def get_user_by_id(user_id : int):
    for U in users:                     # Loop through users list to find user with matching ID
        if U.id == user_id:             # If ID matches, return user data
            return U                    
    return {"error" : "User not found"}     # If not found, raise error

# ------------------------------
# PUT - Update user by ID
# ------------------------------
@app.put("/users/{user_id}")
def update_user(user_id : int, updated_user : User):        # Loop through users list to find user with matching ID
    for index, user in enumerate(users):                    # Loop through users list with index to find user with matching ID
        if user.id == user_id:                              # If ID matches, update user data (except ID which should remain same) and return updated user data
            updated_user.id = user_id                       # Ensure ID remains same (use existing ID from user data)
            users[index] = updated_user                     # Update user data in list (database) with new data
            return {
                "message" : "User Updated",
                "data" : updated_user
            }
    return {"error" : "User not found"}

# ------------------------------
# DELETE - Delete user by ID
# ------------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id : int):
    for index, user in enumerate(users):        # Loop through users list with index to find user with matching ID
        if user.id == user_id:                  # If ID matches, delete user from list (database) and return success message
            users.pop(index)                    # Remove user from list (database) using pop method with index
            return {"message" : "User Deleted"}
    return {"error" : "User not found"}

