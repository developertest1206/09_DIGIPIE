from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine, Base
from routers import user

# ------------------------------
# Lifespan (Modern FastAPI)
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")

    # Create tables (only if not exist)
    Base.metadata.create_all(bind=engine)

    yield

    print("🛑 App shutting down...")

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(lifespan=lifespan)

# ------------------------------
# Include Routers
# ------------------------------
app.include_router(user.router)