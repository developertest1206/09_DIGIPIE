# -----------------------------------------
# IMPORTS
# -----------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------------
# DATABASE CONNECTION URL
# -----------------------------------------
# Format: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/04_LIBRARY_MANAGEMENT_AUTH"

# -----------------------------------------
# CREATE ENGINE: Connects to db like "bridge" between app & DB
# -----------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True       # Shows SQL queries in terminal (for learning/debug)
)

# -----------------------------------------
# SESSION: Used to perform db operations like -insert, update, delete, select
# -----------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,   # we manually save changes
    autoflush=False,    # no auto-save before query
    bind=engine         # connect session with database
)

# -----------------------------------------
# BASE CLASS: Parent Class for all Tables/Models. All models inherit from this
# -----------------------------------------
Base = declarative_base()

# -----------------------------------------
# DEPENDENCY (VERY IMPORTANT)
# -----------------------------------------
def get_db():
    db = SessionLocal()   # create DB session

    try:
        yield db          # give DB to API
    finally:
        db.close()        # close after request