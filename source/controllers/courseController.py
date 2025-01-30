import csv
import io
from flask import Blueprint, jsonify, request
from autho.permission import permission_required
from model.course import Course
from model.grade import Grade
from util import *
from flask_jwt_extended import (
    jwt_required,
)
# Define Blueprint 
courseController = Blueprint("courseController", __name__) 

# --- ROUTES ---

#route to create new course
@courseController.route('/api/course/create',methods=['POST'])
@jwt_required()
@permission_required('create_course')
def create():
    """
    Create a new course.
    Expects JSON payload with course details.
    """
    data = request.json 
    # Validate that the required fields are present and are strings
    if not isinstance(data.get('name'), str) or not data.get('name'):
        return jsonify({"error": "Name must be a non-empty string"}), 422
    
    if not isinstance(data.get('instructor'), str) or not data.get('instructor'):
        return jsonify({"error": "Instructor must be a non-empty string"}), 422
    
    if not isinstance(data.get('semester'), str) or not data.get('semester'):
        return jsonify({"error": "Semester must be a non-empty string"}), 422
    
    # Proceed to save the course if validation passes
    course = Course(**data)
    try:
        course.save()
        return jsonify(success=True, data=serialize(course,[])), 201  
    except ValueError as e:
        return jsonify(error=str(e)), 400  
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500 
    
# Route to retrieve courses with pagination and filtering
@courseController.route("/api/courses", methods=['GET'])
@jwt_required()  
@permission_required('view_courses')  
def get_courses():
    """
    Get a list of courses with optional pagination and  filtering.
    Query Parameters:
      - page: Current page number (default: 1)
      - per_page: Number of users per page (default: 10)
      - semester : Filter by semester 
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    account_type = request.args.get("semester", "All", type=str)
    paginated = Course().get_all(page, per_page, account_type)  
    if paginated:
        start_index = (page - 1) * per_page + 1
        end_index = min(paginated.total, page * per_page)
        courses = [
            serialize(course,[])
                for course in paginated.items
        ]
        results = {
            'courses': courses,
            'pagination': {
                'count': paginated.total,
                'page': page,
                'per_page': per_page,
                'pages': paginated.pages,
                'from': start_index,
                'to':   end_index
            }
        }
        return results 
    else:
         return jsonify({"error": "No Courses Found"}), 404

@courseController.route("/api/course/students", methods=['GET'])
@jwt_required()  
@permission_required('view_courses')  
def get_students():
    """
    Get a list of students enrolled to course with optional pagination.
    Query Parameters:
      - page: Current page number (default: 1)
      - per_page: Number of users per page (default: 10)
      
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    id = request.args.get("course_id", None, type=int)
    if not id:
        return jsonify({"error": "ID required"}), 400
    
    paginated = Course().get_students(page = page, per_page = per_page, course_id = id )  
    if paginated:
        start_index = (page - 1) * per_page + 1
        end_index = min(paginated.total, page * per_page)
        students = [
            serialize(student,[])
                for student in paginated.items
        ]
        results = {
            'students': students,
            'pagination': {
                'count': paginated.total,
                'page': page,
                'per_page': per_page,
                'pages': paginated.pages,
                'from': start_index,
                'to':   end_index
            }
        }
        return results 
    else:
         return jsonify({"error": "No Courses Found"}), 404


from model import db, Grade

@courseController.route("/api/course/grades", methods=['GET'])
@jwt_required()  
@permission_required('view_courses') 
def get_gradings_by_course():
    
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    course_id = request.args.get("course_id", None, type=int)
    if not course_id:
        return jsonify({"error": "ID required"}), 400
    paginated_result = Grade().get_grade( course_id = course_id, page = page, per_page = per_page,)
    result = []
    for grading in paginated_result.items:
        result.append({
            'student_id': grading.student_id,
            'student_name': grading.student.name,
            'student_email': grading.student.email,
            'grade': grading.grade,
            'comment': grading.comment,
        })
    return {
        'data': result,
        'pagination': {
            'page': paginated_result.page,
            'per_page': paginated_result.per_page,
            'total_count': paginated_result.total,
            'total_pages': paginated_result.pages,
        }
    }

@courseController.route("/api/grades/upload", methods=["POST"])
@jwt_required()  
@permission_required('view_courses') 
def upload_grades():
    """
    Upload a CSV file containing grades and insert them into the database.
    Expected CSV format:
      student_id,course_id,grade,comment
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    stream = io.StringIO(file.stream.read().decode("UTF-8"))
    reader = csv.reader(stream)

    headers = next(reader, None)
    if headers and headers != ["student_id", "course_id", "grade", "comment"]:
        return jsonify({"error": "Invalid CSV format"}), 400

    grades_to_insert = []
    for row in reader:
        if len(row) < 3:  
            continue

        student_id = row[0].strip()
        course_id = row[1].strip()
        grade = row[2].strip()
        comment = row[3].strip() if len(row) > 3 else None
        
        if grade not in {"A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"}:
            return jsonify({"error": f"Invalid grade '{grade}' for student {student_id}"}), 400

        grades_to_insert.append(Grade(student_id=student_id, course_id=course_id, grade=grade, comment=comment))

    if grades_to_insert:
        Grade().bulk_insert(grades_to_insert)
        return jsonify({"message": f"{len(grades_to_insert)} grades added successfully!"}), 201
    else:
        return jsonify({"error": "No valid records found in the CSV file"}), 400