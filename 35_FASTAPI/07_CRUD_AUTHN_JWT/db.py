# create_engine for creating a connection to the database
from sqlalchemy import create_engine  
      
# sessionmaker for creating a session factory to interact with the database and from sqlalchemy.ext.declarative import declarative_base     # declarative_base for creating a base class for our models 
from sqlalchemy.orm import sessionmaker, declarative_base   


# ------------------------------SQLITE Connection------------------------------
# Database file path. SQLite means a simple file-based database (like Excel file)
DATABASE_URL = "sqlite:///models.db"

# ------------------------------Create connection (engine)------------------------------
# Create connection between Python and database
# check_same_thread=False means multiple users/requests can use the database safely (important for web apps)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ------------------------------Create session factory------------------------------
SessionLocal = sessionmaker(
    autocommit=False,   # we will manually commit
    autoflush=False,    # no auto save before query
    bind=engine         # connect with database
)


# ------------------------------Base class for models------------------------------
Base = declarative_base()       # declarative_base() is a factory function that constructs a base class for declarative class definitions. This base class maintains a catalog of classes and tables relative to that base, which is used by the ORM to map classes to database tables.


# ------------------------------Dependency (used in APIs)------------------------------
def get_db():
    db = SessionLocal()   # create new DB session
    try:
        yield db          # give session to API
    finally:
        db.close()        # close after request