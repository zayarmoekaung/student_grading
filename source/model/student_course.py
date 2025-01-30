from datetime import timezone
from flask import jsonify
from model import BaseModel,db,func


class StudentCourse(BaseModel):
    __tablename__ = "students_courses"
    id      = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.ForeignKey('students.id'),
        nullable=False,
    )
    course_id = db.Column(
        db.ForeignKey('courses.id'),
        nullable=False,
    )
    enrollmentDate = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )
    student = db.relationship("Student", back_populates="courses")
    course = db.relationship("Course", back_populates="students")
    def __init__(self, student_id=None, course_id=None, enrollmentDate=None):
            self.student_id = student_id
            self.course_id = course_id
            if enrollmentDate:
                self.enrollmentDate = enrollmentDate
    
        
