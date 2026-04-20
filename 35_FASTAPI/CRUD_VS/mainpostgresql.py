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
class Item(SQLModel, table=True):
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

# ✅ GET ALL ITEMS (GET)
@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()  # get all data
        return items

# ✅ GET ITEM BY ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)  # find item by id
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

# ✅ CREATE ITEM (POST)
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)     # add data to DB
        session.commit()      # save changes
        session.refresh(item) # get updated data (id etc.)
        return item

# ✅ UPDATE ITEM (PUT)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    with Session(engine) as session:
        item = session.get(Item, item_id)  # find item
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # update values
        item.name = updated_item.name
        item.email = updated_item.email
        item.is_active = updated_item.is_active

        session.add(item)     # save updated data
        session.commit()
        session.refresh(item)

        return item


# ✅ DELETE ITEM
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)  # find item

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        session.delete(item)   # delete from DB
        session.commit()

        return {"message": "Item deleted successfully"}