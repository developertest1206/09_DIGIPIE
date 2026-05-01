# main.py

from fastapi import FastAPI, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
import os

import models, schema
from db import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Folder to store uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------- SHOW HTML FORM --------------------
@app.get("/", response_class=HTMLResponse)
def show_form():
    
    # Read HTML file and return it
    with open("templates/form.html", "r") as f:
        return f.read()


# -------------------- SUBMIT FORM --------------------
@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    # Create file path
    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    # Save file
    with open(file_path, "wb") as f:
        while chunk := await photo.read(1024):
            f.write(chunk)

    # Save student in database
    new_student = models.Student(
        name=name,
        age=age,
        course=course,
        photo=photo.filename
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message": "Student added successfully"}


# -------------------- GET ALL STUDENTS --------------------
@app.get("/students", response_model=list[schema.StudentOut])
def get_students(db: Session = Depends(get_db)):
    
    students = db.query(models.Student).all()
    return students


# -------------------- VIEW PHOTO --------------------
@app.get("/photo/{filename}")
def get_photo(filename: str):
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(file_path)