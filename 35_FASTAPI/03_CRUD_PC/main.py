from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import user

app = FastAPI()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include router
app.include_router(user.router)