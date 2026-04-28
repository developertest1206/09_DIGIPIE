# Custome Exception Classes: 
# You created your own errors: User not found; Email already exists

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
