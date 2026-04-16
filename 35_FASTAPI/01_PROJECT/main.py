from fastapi import FastAPI         # import FastAPI class to create app instance
from routers import user        # import user router

app = FastAPI()         # create FastAPI app instance

app.include_router(user.router)         # include user router in main app