from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    create_access_token,
    get_jwt
)
from autho.permission import permission_required
from model.user import User

# Define Blueprint 
userController = Blueprint("userController", __name__)

# --- ROUTES ---


# Route to create a new user
@userController.route("/api/user/create", methods=['POST'])
@jwt_required()  
@permission_required('create_user')  
def user_create():
    """
    Create a new user.
    Expects JSON payload with user details.
    """
    data = request.json 
    status = User().create(**data)  
    return status  

# Route to retrieve users with pagination and filtering
@userController.route("/api/users", methods=['GET'])
@jwt_required()  # Require JWT access token
@permission_required('view_users')  # Require specific permission
def get_users():
    """
    Get a list of users with optional pagination and account type filtering.
    Query Parameters:
      - page: Current page number (default: 1)
      - per_page: Number of users per page (default: 10)
      - account_type: Filter by account type (default: "all")
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    account_type = request.args.get("account_type", "All", type=str)
    users = User().get_all(page, per_page, account_type)  # Call User model's get_all method
    return users  # Return the user list

# Route for user login
@userController.route("/api/login", methods=["POST"])
def log_in():
    """
    Log in a user.
    Expects JSON payload with login credentials (e.g., email and password).
    """
    data = request.json  # Get JSON payload from request
    status = User().login(**data)  # Call User model's login method
    return status  # Return status from the model

# Route for user logout
@userController.route("/api/logout", methods=["GET"])
@jwt_required()  # Require JWT access token
def log_out():
    """
    Log out the current user by invalidating their access token.
    """
    jti = get_jwt()["jti"]
    status = User().logout(jti)
    return status
    

