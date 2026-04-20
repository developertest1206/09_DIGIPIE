from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import List

# ------------------ Model ------------------
# This class is used to create a table in the database
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # id is primary key and auto increases
    name: str        # user name (required)
    email: str       # user email (required)
    is_active: bool = False   # default value is False


# ------------------ Database ------------------
# This is the path of your database file
# If file does not exist, it will be created automatically
sqlite_file_name = "D:/09_DIGIPIE/35_FASTAPI/CRUD_VS/mainsqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create connection to database
engine = create_engine(sqlite_url, echo=True)


# This function creates table in database using model
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ------------------ Lifespan ------------------
# This runs when FastAPI app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()   # create table when app starts
    yield


# Create FastAPI app and connect lifespan
app = FastAPI(lifespan=lifespan)

# ------------------ Routes ------------------

# ✅ GET ALL USERS
@app.get("/", response_model=List[User])
def read_users():
    with Session(engine) as session:
        # get all users from database
        users = session.exec(select(User)).all()  

        return users   # return list of users


# ✅ GET USER BY ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    with Session(engine) as session:
        # find user using id
        user = session.get(User, user_id)

        # if user not found, show error
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user


# ✅ CREATE USER
@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)     # add new user to database
        session.commit()      # save changes
        session.refresh(user) # get updated data (like id)

        return user


# ✅ UPDATE USER (PUT)
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    with Session(engine) as session:
        # find existing user
        user = session.get(User, user_id)

        # if user not found, show error
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # update user data
        user.name = updated_user.name
        user.email = updated_user.email
        user.is_active = updated_user.is_active

        session.add(user)     # save updated user
        session.commit()      # commit changes
        session.refresh(user) # get updated data

        return user


# ✅ DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        # find user by id
        user = session.get(User, user_id)

        # if user not found, show error
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)   # delete user from database
        session.commit()       # save changes

        return {"message": "User deleted successfully"}