# clean FastAPI project with: JWT Authentication, Refresh Token, Password Hashing, CRUD APIs


from fastapi import FastAPI

import models, schema
from db import Base, engine
from auth import *





