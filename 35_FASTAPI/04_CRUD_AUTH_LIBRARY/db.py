# ----------------------------------------
# IMPORTS
# ----------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------------------
# DATABASE URL
# ----------------------------------------
# Change this only based on your database

# PostgreSQL
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/04_CRUD_AUTH_LIBRARY"

# MySQL
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/db_name"

# SQLite (for testing)
# DATABASE_URL = "sqlite:///./test.db"


# ----------------------------------------
# CREATE ENGINE (CONNECT DATABASE)
# ----------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=False   # shows SQL queries in terminal (good for debugging)
)


# ----------------------------------------
# SESSION (FOR DB OPERATIONS)
# ----------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ----------------------------------------
# BASE CLASS (FOR MODELS)
# ----------------------------------------
Base = declarative_base()


# ----------------------------------------
# DEPENDENCY (IMPORTANT 🔥)
# ----------------------------------------
# This function gives DB session to API and closes it after request

def get_db():
    db = SessionLocal()
    try:
        yield db   # give DB session
    finally:
        db.close()  # close connection