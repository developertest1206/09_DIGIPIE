from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import UserNotFoundException, UserAlreadyExistsException
from routers import user
from db import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)



# Handle User Not Found
@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"User with ID {exc.user_id} not found."}
    )

@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={"message" : f"User with email {exc.email} already exists."}
    )


@app.get("/")
def home():
    return {"message": "API running..."}