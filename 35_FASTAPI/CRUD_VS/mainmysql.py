from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# ------------------ DATABASE URL ------------------
# Format: mysql+pymysql://username:password@host:port/database_name

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/CRUD_VS"
# 👉 Make sure:
# - MySQL is running
# - Database "FastAPI_DB" already created in MySQL Workbench

# ------------------ MODEL ------------------
# This class will create a table in MySQL
class mainmysql_user(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)   # id = primary key, auto increment
    name: str        # user name
    email: str       # user email
    is_active: bool = False   # default = False


# ------------------ DATABASE CONNECTION ------------------
# Connect FastAPI to MySQL
engine = create_engine(DATABASE_URL, echo=True)


# ------------------ CREATE TABLE ------------------
# This will create table automatically when app starts
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ------------------ LIFESPAN ------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()   # create table
    yield


# ------------------ APP ------------------
app = FastAPI(lifespan=lifespan)


# ------------------ ROUTES ------------------

# ✅ CREATE USER
@app.post("/user/", response_model=mainmysql_user)
def create_users(user: mainmysql_user):
    with Session(engine) as session:
        session.add(user)     # add data
        session.commit()      # save
        session.refresh(user) # get id
        return user


# ✅ GET ALL USER
@app.get("/users/", response_model=List[mainmysql_user])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(mainmysql_user)).all()
        return users


# ✅ GET USER BY ID
@app.get("/user/{user_id}", response_model=mainmysql_user)
def read_users(user_id: int):
    with Session(engine) as session:
        users = session.get(mainmysql_user, user_id)

        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        return users


# ✅ UPDATE USER
@app.put("/user/{user_id}", response_model=mainmysql_user)
def update_users(user_id: int, updated_user: mainmysql_user):
    with Session(engine) as session:
        user = session.get(mainmysql_user, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.name = updated_user.name
        user.email = updated_user.email
        user.is_active = updated_user.is_active

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


# ✅ DELETE USER
@app.delete("/user/{user_id}")
def delete_users(user_id: int):
    with Session(engine) as session:
        user = session.get(mainmysql_user, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}