from datetime import timezone
from flask import jsonify
from model import BaseModel,db,func

class Grade(BaseModel):
    __tablename__ = "grades"
    id      = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.ForeignKey('students.id'),
        nullable=False,
    )
    course_id = db.Column(
        db.ForeignKey('courses.id'),
        nullable=False,
    )
    grade = db.Column(db.String(3),nullable=False)
    comment = db.Column(db.String(255),nullable=True)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )
    student = db.relationship("Student", back_populates="grades")
    course = db.relationship("Course", back_populates="grades")
    
    def __init__(self, student_id=None, course_id=None, grade=None, comment=None):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.comment = comment
        
    def get_grade(self,course_id: int = None, page: int = 1, per_page: int = 10):
        query = db.session.query(Grade).filter(Grade.course_id == course_id)    
        paginated_result = query.paginate(page=page, per_page=per_page, error_out=False)
        return paginated_result
    
    def bulk_insert(self,grades):
        db.session.bulk_save_objects(grades)
        db.session.commit()
        