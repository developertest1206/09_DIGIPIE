from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# ------------------ DATABASE URL ------------------
# Format: mysql+pymysql://username:password@host:port/database_name

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/FastAPI_DB"
# 👉 Make sure:
# - MySQL is running
# - Database "FastAPI_DB" already created in MySQL Workbench

# ------------------ MODEL ------------------
# This class will create a table in MySQL
class User(SQLModel, table=True):
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

# ✅ CREATE ITEM
@app.post("/items/", response_model=User)
def create_item(item: User):
    with Session(engine) as session:
        session.add(item)     # add data
        session.commit()      # save
        session.refresh(item) # get id
        return item


# ✅ GET ALL ITEMS
@app.get("/items/", response_model=List[User])
def read_items():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users


# ✅ GET ITEM BY ID
@app.get("/items/{item_id}", response_model=User)
def read_item(item_id: int):
    with Session(engine) as session:
        users = session.get(User, item_id)

        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        return users


# ✅ UPDATE ITEM
@app.put("/items/{item_id}", response_model=User)
def update_item(item_id: int, updated_item: User):
    with Session(engine) as session:
        user = session.get(User, item_id)

        if not user:
            raise HTTPException(status_code=404, detail="Item not found")

        user.name = updated_item.name
        user.email = updated_item.email
        user.is_active = updated_item.is_active

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


# ✅ DELETE ITEM
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        user = session.get(User, item_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}