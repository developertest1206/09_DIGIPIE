from sqlalchemy import Table, Column, Integer, String
from db import metadata   # import metadata from database.py

# Create table "employees"
employee = Table(
    "employees",   # table name in MySQL
    metadata,      # link table with metadata
    Column("id", Integer, primary_key=True),    # id column (primary key)
    Column("name", String(50), unique=True, nullable=False, index=True),    # name must be unique, cannot be empty
    Column("password", String(255), nullable=False)      # password column
)