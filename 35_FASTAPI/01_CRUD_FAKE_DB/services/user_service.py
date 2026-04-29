from db import users_db

# CREATE USER
def create_user_service(user):
    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email
    }
    users_db.append(new_user)
    return new_user


from db import users_db

# ---------------- CREATE USER ----------------
# This function creates a new user and saves it in the list (database)
def create_user_service(user):

    # Create a new user with id, name and email. 
    new_user = {
        "id": len(users_db) + 1,       # Generate new user id by taking length of users_db and adding 1
        "name": user.name,
        "email": user.email
    }

    # Add new user into database list
    users_db.append(new_user)

    # Return created user
    return new_user


# ---------------- GET ALL USERS ----------------
# This function returns all users from the list
def get_all_users_service():
    return users_db



# ---------------- GET SINGLE USER ----------------
# This function finds one user using user_id
def get_user_service(user_id):

    # Loop through all users
    for user in users_db:

        # If id matches, return that user
        if user["id"] == user_id:
            return user

    # If not found, return None (means no user)
    return None      



# ---------------- UPDATE USER ----------------
# This function updates user details using user_id
def update_user_service(user_id, updated_user):

    # Loop through all users
    for user in users_db:

        # Find matching user
        if user["id"] == user_id:

            # Update name and email
            user["name"] = updated_user.name
            user["email"] = updated_user.email

            # Return updated user
            return user

    # If user not found
    return None  




# ---------------- DELETE USER ----------------
# This function deletes user using user_id
def delete_user_service(user_id):

    # Loop with index (position) and user
    for index, user in enumerate(users_db):

        # Find matching user
        if user["id"] == user_id:

            # Remove user from list
            users_db.pop(index)

            # Return True means success
            return True

    # If user not found
    return False
