# This is our custom exception class
class StudentNotFoundException(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id