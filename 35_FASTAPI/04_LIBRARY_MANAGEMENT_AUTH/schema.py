from pydantic import BaseModel, EmailStr
from typing import List
import datetime

# ------------------------- USER -------------------------
# This is used when a new user registers. It defines what data the user must send
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str 

# This is used when user logs in
class UserLogin(BaseModel):     
    email: EmailStr
    password: str

# This is used to SHOW user data (response). Password is NOT included for security
class User(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True     # Convert DB object → JSON

# ------------------------- BOOK -------------------------
# This is used when creating a new book
class BookCreate(BaseModel): 
    title: str
    author: str
    user_id: int

# This is used to SHOW all book data
class Book(BaseModel): 
    id: int     
    title: str
    author: str 
    published_date: datetime.datetime       # Date when book was added
    user_id: int                            # Owner ID
    user: User     # Shows full user details inside book

    class Config:
        orm_mode = True

# This is a simple version of book (without user info). Used when we don't need full user details
class Books(BaseModel): 
    id: int     
    title: str
    author: str 
    published_date: datetime.datetime

    class Config:
        orm_mode = True

# =========================================
# 🔗 NESTED SCHEMAS (RELATIONSHIP)
# =========================================
# ------------------------- USER With BOOK -------------------------
# Show user with ALL their books. Example: "User + list of books"
class UserWithBook(BaseModel):          # show user + all books
    id: int
    name: str
    email: EmailStr

    books : List[Books] = []     # One user → many books

    class Config:
        orm_mode = True

# ------------------------- BOOK With USER -------------------------
# Show book with its owner (user). Example: "Book + user details"
class BookWithUser(BaseModel):          # show book + owner
    id: int
    title: str
    author: str

    user:User       # One book → one user

    class Config:
        orm_mode = True