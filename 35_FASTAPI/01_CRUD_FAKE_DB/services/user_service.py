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


# GET ALL USERS
def get_all_users_service():
    return users_db


# GET SINGLE USER
def get_user_service(user_id):
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None        


# UPDATE USER
def update_user_service(user_id, updated_user):
    for user in users_db:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return user
    return None  


# DELETE USER
def delete_user_service(user_id):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(index)
            return True
    return False