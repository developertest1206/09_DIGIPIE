from database import users_db      # import fake DB (list)


# CREATE USER
def create_user_service(user):
    new_user = {
        "id": len(users_db) + 1,   # auto increment id
        "name": user.name,         # get name from request
        "email": user.email        # get email from request
    }
    users_db.append(new_user)      # store in fake DB
    return new_user                # return created user


# GET ALL USERS
def get_all_users_service():
    return users_db                # return full list


# GET SINGLE USER
def get_user_service(user_id):
    for user in users_db:          # loop through users
        if user["id"] == user_id:  # check id
            return user
    return {"error" : 404, "message" : "User Not Found."}                    # not found


# UPDATE USER
def update_user_service(user_id, updated_user):
    for user in users_db:
        if user["id"] == user_id:
            user["name"] = updated_user.name   # update name
            user["email"] = updated_user.email # update email
            return user
    return {"error" : 404, "message" : "User Not Found."}                    # not found


# DELETE USER
def delete_user_service(user_id):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(index)   # remove user
            return {"message": "User deleted successfully"}  # success
    # if loop completes and no match found
    return {"error": 404, "message": "User Not Found."}