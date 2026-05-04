# Import os to read environment variables
import os

# Import load_dotenv to load .env file
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Read variables from .env

# This reads SECRET_KEY from .env
SECRET_KEY = os.getenv("SECRET_KEY")

# This reads APP_NAME
APP_NAME = os.getenv("APP_NAME")

# This reads ADMIN_EMAIL
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")