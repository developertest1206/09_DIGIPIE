from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db import engine, Base
import models
from routers import student
from exceptions import StudentNotFoundException

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student.router)


# 🔥 GLOBAL EXCEPTION HANDLER
@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(request: Request, exc: StudentNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Student not found",
            "student_id": exc.student_id
        }
    )


@app.get("/")
def home():
    return {"message": "Student API Running..."}