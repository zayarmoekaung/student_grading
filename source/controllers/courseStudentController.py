from flask import Blueprint, jsonify, request
from autho.permission import permission_required
from model.course import Course
from model.student import Student
from model.student_course import StudentCourse
from util import *
from flask_jwt_extended import (
    jwt_required,
)
# Define Blueprint 
courseStudentController = Blueprint("courseStudentController", __name__) 

# --- ROUTES ---

#route to enroll students
@courseStudentController.route('/api/course/enroll',methods=['POST'])
@jwt_required()
@permission_required('enroll_student')
def enroll():
    """
        Create a new course.
        Expects JSON payload with course and student IDs.
    """
    data = request.json 
    if not isinstance(data.get('course_id'), str) or not data.get('course_id'):
        return jsonify({"error": "Course Id must be a non-empty string"}), 422
    if not isinstance(data.get('student_id'), str) or not data.get('student_id'):
        return jsonify({"error": "Student ID must be a non-empty string"}), 422
    
    student = Student.search_by_studentID(data.get('student_id'))
    course = Course.search_by_courseID(data.get('course_id'))
    
    if not student:
        return jsonify({"error": "Student Not Found"}), 404
    if not course:
        return jsonify({"error": "Course Not Found"}), 404
    
    course_id = course.id
    student_id = student.id
    
    enrollment = StudentCourse(student_id,course_id)
    try:
        enrollment.save()
        return jsonify(success=True), 201  
    except ValueError as e:
        return jsonify(error=str(e)), 400  
    except Exception as e:
        return jsonify(error="An unexpected error occurred."), 500 
    