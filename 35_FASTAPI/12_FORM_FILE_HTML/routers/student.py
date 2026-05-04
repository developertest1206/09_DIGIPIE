# APIRouter → used to group related APIs (like student APIs)
# Form → used to receive normal form data (text, numbers)
# UploadFile, File → used to receive file (like image)
# Depends → used to connect database
from fastapi import APIRouter, Form, UploadFile, File, Depends

# HTMLResponse → used to return HTML page
# FileResponse → used to return file (like image)
from fastapi.responses import HTMLResponse, FileResponse

# Session → used to talk with database  
from sqlalchemy.orm import Session

# os → used to work with folders and file paths
import os

# Import database models and schema
import models, schema

# Import database connection
from db import engine, get_db


# Create router for student APIs
# prefix="/student" means all APIs will start with /student
# tags=["Student"] helps group APIs in Swagger UI
router = APIRouter(prefix="", tags=["Student"])


# Folder to store uploaded images
UPLOAD_FOLDER = "uploads"

# Create folder if it does not already exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- SHOW HTML FORM --------------------
# This API will show a HTML form in browser
@router.get("/", response_class=HTMLResponse)
def show_form():
    
    # Open the HTML file from templates folder
    with open("templates/form.html", "r") as f:
        
        # Return HTML content to browser
        return f.read()


# -------------------- SUBMIT FORM --------------------
# This API will receive form data + image and save it
@router.post("/submit")
async def submit_form(
    name: str = Form(...),          # Get student name from form
    age: int = Form(...),           # Get age from form
    course: str = Form(...),        # Get course from form
    photo: UploadFile = File(...),  # Get uploaded photo file
    db: Session = Depends(get_db)   # Connect to database
):
    
    # Create full file path (example: uploads/photo.png)
    file_path = os.path.join(UPLOAD_FOLDER, photo.filename)

    # Open file in write mode (wb = write binary)
    with open(file_path, "wb") as f:
        # Read file in small parts and save (good for large files)
        while chunk := await photo.read(1024):
            f.write(chunk)

    # Create new student object to save in database
    new_student = models.Student(
        name=name,
        age=age,
        course=course,
        photo=photo.filename     # Save only file name in DB
    )

    db.add(new_student)       # Add student to database
    db.commit()               # Save changes permanently
    db.refresh(new_student)   # Refresh to get updated data (like id)

    return {"message": "Student added successfully"}         # Return success message


# -------------------- GET ALL STUDENTS --------------------
# This API will return all students from database
@router.get("/students", response_model=list[schema.StudentOut])
def get_students(db: Session = Depends(get_db)):
    
    # Get all student records
    students = db.query(models.Student).all()

    # Return list of students
    return students


# -------------------- VIEW PHOTO --------------------
# This API will show uploaded image in browser
@router.get("/photo/{filename}")
def get_photo(filename: str):
    
    # Create full path of file
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Return image file to browser
    return FileResponse(file_path)