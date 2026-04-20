from sqlalchemy import create_engine                # create_engine is a function that creates a new SQLAlchemy engine instance
from sqlalchemy.ext.declarative import declarative_base # declarative_base is a function that returns a new base class from which all mapped classes should inherit
from sqlalchemy.orm import sessionmaker             # sessionmaker is a function that creates a new SQLAlchemy session factory

# ------------------------------
# PostgreSQL URL
# ------------------------------
# Format:
# postgresql://username:password@localhost:port/db_name

PostgreSQL_DB_URL = "postgresql://postgres:admin123@localhost:5432/FastAPI_DB"

# ------------------------------
# Create SQLAlchemy engine
# ------------------------------
engine = create_engine(PostgreSQL_DB_URL)

# ------------------------------
# Create Session (DB operations)
# ------------------------------
# sessionmaker is a factory for creating new Session objects. It takes the engine as an argument to bind the session to the database.
# autocommit=False means that the session will not automatically commit transactions. You will need to call session.commit() explicitly to save changes to the database.
# autoflush=False means that the session will not automatically flush changes to the database before executing queries. You will need to call session.flush() explicitly to send changes to the database.
# bind=engine means that the session will be bound to the engine we created earlier, allowing it to connect to the PostgreSQL database.
SessionLocal = sessionmaker(
    autocommit=False,           
    autoflush=False,            
    bind=engine             
)

# ------------------------------
# Base class for models
# ------------------------------
Base = declarative_base()       # declarative_base() is a factory function that constructs a base class for declarative class definitions. This base class maintains a catalog of classes and tables relative to that base, which is used by the ORM to map classes to database tables.


# ------------------------------
# Dependency for DB session
# ------------------------------
# This function is a dependency that can be used in FastAPI endpoints to get a database session. It creates a new session using the SessionLocal 
# factory, yields it for use in the endpoint, and then ensures that the session is closed after the endpoint is finished.                                
def get_db():               
    db = SessionLocal()     
    try:
        yield db        # Yielding the database session allows it to be used in FastAPI endpoints as a dependency. 
        # The endpoint can perform database operations using this session, and once the endpoint is done, the session will be closed in the finally block to ensure that resources are properly released.
    finally:
        db.close()