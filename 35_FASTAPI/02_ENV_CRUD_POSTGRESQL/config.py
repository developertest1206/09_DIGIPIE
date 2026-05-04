# Import os to read environment variables
import os

# Import load_dotenv to load .env file
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Read variables from .env

# This reads DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")