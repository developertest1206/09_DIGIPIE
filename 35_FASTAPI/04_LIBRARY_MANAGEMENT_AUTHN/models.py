# -----------------------------------------
# IMPORTS
# -----------------------------------------
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
import datetime

# =========================================
# USER TABLE
# =========================================
class Users(Base):
    __tablename__ = "users"

    # ------------------------- COLUMNS -------------------------
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now)

    # ------------------------- RELATIONSHIP -------------------------
    books = relationship("Books", back_populates="user")         # One user → many books. Example: user.books → list of books

# =========================================
# BOOK TABLE
# =========================================
class Books(Base):
    __tablename__ = "books"

    # ------------------------- COLUMNS -------------------------
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    published_date = Column(DateTime, default=datetime.datetime.now)         # automatically store date & time

    # ------------------------- FOREIGN KEY (IMPORTANT) -------------------------
    user_id = Column(Integer, ForeignKey("users.id"))           # This connects book → user

    # ------------------------- RELATIONSHIP -------------------------
    user = relationship("Users", back_populates="books")        # Many books → one user