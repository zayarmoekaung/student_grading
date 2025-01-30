from datetime import datetime
import os
from model import BaseModel,db,func
from dotenv import load_dotenv


load_dotenv()

class Student(BaseModel):
    __tablename__ = "students"
    id      = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.String(15),unique=True,nullable=False)
    name    = db.Column(db.String(30),nullable=False)
    email   = db.Column(db.String(30),unique=True,nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )
    courses = db.relationship("StudentCourse", back_populates="student")
    grades = db.relationship("Grade", back_populates="student")
    def __init__(self, name=None, email=None, studentID=None):
        """Generate New Student ID"""
        prefix = os.getenv("STUDENT_ID_PREFIX", "STU")[:3].upper()
        date_part = datetime.now().strftime("%Y%m")
        total_students = db.session.query(db.func.count(Student.id)).scalar()
        student_number = total_students + 1
        self.studentID = f"{prefix}{date_part}{student_number:04d}"
        
        self.name = name
        self.email = email
    
    @classmethod
    def search_by_studentID(cls, studentID):
        """Search for a student by studentID."""
        student = cls.query.filter_by(studentID=studentID).first()
        if student:
            return student
        else:
            return None
    
        
