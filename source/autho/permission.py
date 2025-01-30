from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from model.user import User
from .rules import PERMISSIONS

class Permission:
    def __init__(self, user_id):
        self.role = None
        self.permissions = PERMISSIONS
        user = User().get_by_id(user_id)
        if user and user.role:
            self.role = user.role

    def has_permission(self, permission):
        if self.role:
            return self.role in self.permissions.get(permission, [])
        return False


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            permission = Permission(user)
            if permission.has_permission(permission_name):
                return func(*args, **kwargs)
            return jsonify({"message": "Access Denied","attempted role": permission.role}), 401
        return wrapper
    return decorator




            
        
        