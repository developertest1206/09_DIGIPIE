# Import tools for token creation, time handling, and password security
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Secret key is used to lock and unlock the token (like a password for token)
SECRET_KEY = "mysecretkey"

# Algorithm used to create token (method of encryption)
ALGORITHM = "HS256"


# This is used to convert password into a secure format (hash) and to verify password during login
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------- PASSWORD HASH --------

# This function converts normal password into secure unreadable format
def hash_password(password: str):
    return pwd_context.hash(password)

# This function checks if the password entered by user is correct by comparing it with the hased password stored in database
def verify_password(plain, hased):
    return pwd_context.verify(plain, hased)





# -------- TOKEN CREATION --------
# This function creates a token (like a login pass)
def create_token(data:dict):
    to_encode = data.copy()                              # Copy user data (example: username) into new variable (don't change original data)
    expire = datetime.utcnow() + timedelta(minutes=30)      # Set expiry time (token valid for 30 minutes)
    to_encode.update({"exp" : expire})                   # Add expiry time into data (so we can check it later when user sends token)
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  #create token using user data, secret key and algorithm
    return token                               # Return the created token to user (so they can use it in future requests)              



# -------- TOKEN VERIFY --------
# This function checks if token is valid or not (not fake, not expired)
def verify_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)       # Decode token using same secret key and algorithm (if token is fake or expired, it will show error) 
        return payload        # If token is correct, return user data (payload)
    except JWTError:
        return None     # If token is wrong, expired, or fake → return None 