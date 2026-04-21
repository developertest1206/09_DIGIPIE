from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# ------------------ Database URL ------------------
# This is PostgreSQL connection (just like SQLite file, but here it's a server DB)
# Format: postgresql://username:password@host:port/database_name
PostgreSQL_DB_URL = "postgresql://postgres:admin123@localhost:5432/FastAPI_DB"


# ------------------ Model ------------------
# This class = table in database (same like SQLite table)
class mainpostgresql(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # id is primary key and auto increases
    name: str        # user name (required)
    email: str       # user email (required)
    is_active: bool = False   # default value is False


# ------------------ Database Connection ------------------
# This connects your FastAPI app to PostgreSQL database
engine = create_engine(PostgreSQL_DB_URL, echo=True)


# ------------------ Create Table ------------------
# This will automatically create table in DB if not exists
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ------------------ Lifespan ------------------
# This runs when FastAPI app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()   # create table
    yield


# ------------------ App ------------------
app = FastAPI(lifespan=lifespan)


# ------------------ Routes ------------------

# ✅ GET ALL User (GET)
@app.get("/user/", response_model=List[mainpostgresql])
def read_user():
    with Session(engine) as session:
        user = session.exec(select(mainpostgresql)).all()  # get all data
        return user

# ✅ GET User BY ID
@app.get("/user/{user_id}", response_model=mainpostgresql)
def read_user(user_id: int):
    with Session(engine) as session:
        user = session.get(mainpostgresql, user_id)  # find mainpostgresql by id
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

# ✅ CREATE User (POST)
@app.post("/user/", response_model=mainpostgresql)
def create_item(user: mainpostgresql):
    with Session(engine) as session:
        session.add(user)     # add data to DB
        session.commit()      # save changes
        session.refresh(user) # get updated data (id etc.)
        return user

# ✅ UPDATE User (PUT)
@app.put("/user/{user_id}", response_model=mainpostgresql)
def update_item(user_id: int, updated_user: mainpostgresql):
    with Session(engine) as session:
        user = session.get(mainpostgresql, user_id)  # find user
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # update values
        user.name = updated_user.name
        user.email = updated_user.email
        user.is_active = updated_user.is_active

        session.add(user)     # save updated data
        session.commit()
        session.refresh(user)

        return user


# ✅ DELETE User
@app.delete("/user/{user_id}")
def delete_item(user_id: int):
    with Session(engine) as session:
        user = session.get(user, user_id)  # find user

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)   # delete from DB
        session.commit()

        return {"message": "User deleted successfully"}