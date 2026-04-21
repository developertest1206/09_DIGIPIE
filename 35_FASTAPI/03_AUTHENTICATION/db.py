from sqlalchemy import create_engine, MetaData      # Import tools to connect database
from databases import Database   # Import async database connection tool for FastAPI

# MySQL connection URL
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/FastAPI_DB"

# This is async database connection (used in FastAPI)
database = Database(DATABASE_URL)

# Metadata stores table structure (used by SQLAlchemy)
metadata = MetaData()

# Engine is used to connect and run SQL commands
engine = create_engine(DATABASE_URL)