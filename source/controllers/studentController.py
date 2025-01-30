from flask import Blueprint, jsonify, request
from autho.permission import permission_required
from model.student import Student
from util import *
from flask_jwt_extended import (
    jwt_required,
)
# Define Blueprint 
studentController = Blueprint("studentController", __name__) 

# --- ROUTES ---

#route to create new student
@studentController.route('/api/student/create',methods=['POST'])
@jwt_required()
@permission_required('create_student')
def create():
    """
    Create a new student.
    Expects JSON payload with course details.
    """
    data = request.json 
    # Validate that the required fields are present and are strings
    if not isinstance(data.get('name'), str) or not data.get('name'):
        return jsonify({"error": "Name must be a non-empty string"}), 422
    if not isinstance(data.get('email'), str) or not data.get('name'):
        return jsonify({"error": "Email must be a non-empty string"}), 422
    
    # Proceed to save the student if validation passes
    student = Student(**data)
    try:
        student.save()
        return jsonify(success=True, data=serialize(student,[])), 201  
    except ValueError as e:
        return jsonify(error=str(e)), 400  
    except Exception as e:
        return jsonify(error="An unexpected error occurred."), 500 