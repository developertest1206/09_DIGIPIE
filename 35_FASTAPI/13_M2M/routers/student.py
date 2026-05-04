# APIRouter → used to group related APIs (like student APIs)
# Depends → used to connect database
# HTTPException → used to show error
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session          # Session → used to talk with database  
import models, schema                       # Import database models and schem
from db import get_db                       # Import database connection

router = APIRouter(prefix="/students", tags=["Student"])


# ---------------- CREATE STUDENT ----------------
@router.post("/")
def create_student(student: schema.StudentCreate, db: Session = Depends(get_db)):

    # Create a new student object using name from request
    new_student = models.Student(name=student.name)

    db.add(new_student)     # Add student to database
    db.commit()             # Save changes in database
    db.refresh(new_student) # Refresh to get updated data (like id)

    return new_student    # Return created student


# ---------------- CREATE COURSE ----------------
@router.post("/course")
def create_course(course: schema.CourseCreate, db: Session = Depends(get_db)):
    
    # Create new course object
    new_course = models.Course(title = course.title)

    db.add(new_course)      # Add course to database
    db.commit()             # Save changes in database
    db.refresh(new_course)  # Refresh to get id

    return new_course       # Return created course


# ---------------- ASSIGN COURSE TO STUDENT ----------------
@router.post("/{student_id}/add-course/{course_id}", response_model=schema.StudentOut)
def add_course(student_id: int, course_id: int, db: Session = Depends(get_db)):

    # Find student from database using student_id
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    # If student not found, show error
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Find course from database using course_id
    course = db.query(models.Course).filter(models.Course.id == course_id).first()

    # If course not found, show error
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Connect student and course (many-to-many relation)
    # This means: add this course to student's course list
    student.courses.append(course)

    # Save changes in database
    db.commit()

    # Refresh student to get updated data (with courses)
    db.refresh(student)

    # Return updated student data (with assigned course)
    return student


# ---------------- GET ALL STUDENTS ----------------
@router.get("/", response_model=list[schema.StudentOut])
def get_students(db: Session = Depends(get_db)):

    # Get all students from database (with courses)
    return db.query(models.Student).all()


# ---------------- DELETE STUDENT ----------------
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    # Find student by id
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    # If not found, show error
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)      # Delete student from database
    db.commit()             # Save changes

    return {"message": "Student deleted"}