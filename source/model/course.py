import os
from datetime import datetime
from model import BaseModel,db,func
from dotenv import load_dotenv
from model.student import Student
from model.student_course import StudentCourse
load_dotenv()

class Course(BaseModel):
    __tablename__   = "courses"
    id      = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.String(15),unique=True,nullable=False)
    name     = db.Column(db.String(30),nullable=False)
    instructor     = db.Column(db.String(30),nullable=False)
    semester     = db.Column(db.String(30),nullable=False)
    created_at = db.Column(
    db.DateTime,
    server_default=func.now(),
    nullable=False,
    )

    students = db.relationship("StudentCourse", back_populates="course")
    grades = db.relationship("Grade", back_populates="course")

    def __init__(self, name = None, instructor = None, semester = None):
            """Generate New Course ID"""
            prefix = os.getenv("COURSE_ID_PREFIX", "COU")[:3].upper()  
            date_part = datetime.now().strftime("%Y%m")  
            total_courses = db.session.query(db.func.count(Course.id)).scalar()  
            course_number = total_courses + 1
            self.courseID = f"{prefix}{date_part}{course_number:04d}"
            
            self.name = name
            self.instructor = instructor
            self.semester = semester
    
    @classmethod
    def search_by_courseID(cls, courseID):
        """Search for a course by its courseID."""
        course = cls.query.filter_by(courseID=courseID).first()
        if course:
            return course
        else:
            return None 
    
    def get_all(self,page,per_page,semester):
        """Get all courses"""
        if self.query.all():
            query = self.query
            query = query.order_by(Course.created_at)
            if semester != "All":
                query = query.filter_by(semester=semester)
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            return paginated
        return 0
        
    def get_students(self, page=1, per_page=10, course_id=None):
        if not course_id:
            return None  

        paginated = (
            db.session.query(Student)
            .join(StudentCourse)  
            .filter(StudentCourse.course_id == course_id)  
            .order_by(StudentCourse.enrollmentDate.desc())  
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        
        return paginated
    