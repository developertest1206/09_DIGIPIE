# Import required tools from SQLAlchemy
from sqlalchemy import create_engine        # create_engine for creating a connection to the database
from sqlalchemy.ext.declarative import declarative_base     # declarative_base for creating a base class for our models 
from sqlalchemy.orm import sessionmaker     # sessionmaker for creating a session factory to interact with the database

# ------------------ MYSQL DATABASE URL ------------------
# Format:   postgresql://username:password@localhost:port/db_name
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/03_CRUD_AUTHENTICATION_MYSQL"

# ------------------ ENGINE ------------------
# This connects Python to MySQL
engine = create_engine(DATABASE_URL, echo=True)

# ------------------ SESSION ------------------
# This is used to talk with the database (CRUD operations)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------ BASE ------------------
# All models (tables) will inherit from this
Base = declarative_base() 


# ------------------ DEPENDENCY ------------------
# Used in FastAPI routes to get DB session
def get_db():
    db = SessionLocal()   # create new DB session
    try:
        yield db          # give session to API
    finally:
        db.close()        # close after request