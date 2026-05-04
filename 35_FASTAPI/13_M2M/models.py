from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# ---------------- M2M TABLE ----------------
# This is a helper table to connect students and courses
# One student can have many courses
# One course can have many students
student_course = Table(
    "student_course",
    Base.metadata,

    # store student id
    Column("student_id", Integer, ForeignKey("students.id")),

    # store course id
    Column("course_id", Integer, ForeignKey("courses.id"))
)

# ---------------- STUDENT TABLE ----------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)  # unique id
    name = Column(String)                               # student name

    # relation with Course (many-to-many)
    courses = relationship(
        "Course",                    # connect to Course table
        secondary=student_course,    # use helper table
        back_populates="students"    # reverse link
    )

# ---------------- COURSE TABLE ----------------
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)  # unique id
    title = Column(String)                              # course name

    # relation with Student (many-to-many)
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )