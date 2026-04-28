from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import models, schema
from exceptions import StudentNotFoundException

router = APIRouter(prefix="/students", tags=["Students"])


# ------------------ CREATE ------------------
@router.post("/")
def create_student(student: schema.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(name=student.name)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# ------------------ GET ALL ------------------
@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# ------------------ GET BY ID ------------------
@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    # Instead of HTTPException
    if not student:
        raise StudentNotFoundException(student_id)   # custom exception

    return student