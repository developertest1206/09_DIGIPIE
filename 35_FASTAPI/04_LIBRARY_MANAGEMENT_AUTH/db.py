# create_engine for creating a connection to the database
from sqlalchemy import create_engine  
      
# sessionmaker for creating a session factory to interact with the database and from sqlalchemy.ext.declarative import declarative_base     # declarative_base for creating a base class for our models 
from sqlalchemy.orm import sessionmaker, declarative_base   


# ------------------------------DATABASE CONNECTION URL------------------------------
# Format: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/04_LIBRARY_MANAGEMENT_AUTH"


# ------------------------------Create connection (engine)------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True       # Shows SQL queries in terminal (for learning/debug)
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