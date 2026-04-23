# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List


# ------------------ DATABASE URL ------------------
# Format: postgresql://username:password@host:port/database
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/CRUD_VS"


# ------------------ MODEL (TABLE) ------------------
# This class will create a table in PostgreSQL
class mainpostgresql_user(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Auto ID
    name: str        # User name
    email: str       # User email
    is_active: bool = False   # Default = False


# ------------------ DATABASE CONNECTION ------------------
engine = create_engine(DATABASE_URL, echo=True)


# ------------------ CREATE TABLE ------------------
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# ------------------ APP STARTUP ------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()   # Create table when app starts
    yield


# ------------------ FASTAPI APP ------------------
app = FastAPI(lifespan=lifespan)


# =========================================================
# ===================== ROUTES =============================
# =========================================================

# ✅ GET ALL USERS
@app.get("/user/", response_model=List[mainpostgresql_user])
def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(mainpostgresql_user)).all()
        return users


# ✅ GET USER BY ID
@app.get("/user/{user_id}", response_model=mainpostgresql_user)
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.get(mainpostgresql_user, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user


# ✅ CREATE USER
@app.post("/user/", response_model=mainpostgresql_user)
def create_user(user: mainpostgresql_user):
    with Session(engine) as session:
        session.add(user)      # Add data
        session.commit()       # Save to DB
        session.refresh(user)  # Get updated data (like ID)
        return user


# ✅ UPDATE USER
@app.put("/user/{user_id}", response_model=mainpostgresql_user)
def update_user(user_id: int, updated_user: mainpostgresql_user):
    with Session(engine) as session:
        user = session.get(mainpostgresql_user, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update values
        user.name = updated_user.name
        user.email = updated_user.email
        user.is_active = updated_user.is_active

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


# ✅ DELETE USER
@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(mainpostgresql_user, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}