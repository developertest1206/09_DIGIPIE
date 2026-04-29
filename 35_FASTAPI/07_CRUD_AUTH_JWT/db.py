# Import tools needed to connect Python with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database file path. SQLite means a simple file-based database (like Excel file)
DATABASE_URL = "sqlite:///models.db"


# Create connection between Python and database
# check_same_thread=False means multiple users/requests can use the database safely (important for web apps)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Session = a temporary connection to the database, used to perform operations (like add, query, delete)
SessionLocal = sessionmaker(
    autocommit=False,   # Changes will not save automatically (important for data integrity)
    autoflush=False,    # Data will not send automatically to database (important for performance)
    bind=engine         # Connect session with database engine 
)


# Base class used to create tables (All models/tables will be created using this)
Base = declarative_base()


# This function gives database connection when needed
def get_db():
    db = SessionLocal()   # Open database connection

    try:
        yield db          # Give connection to API (use it)
    
    finally:
        db.close()        # Close connection after work is done