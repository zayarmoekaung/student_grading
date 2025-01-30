from datetime import timezone
from flask import jsonify

from model.token import TokenBlocklist
from .model import db,deferred,datetime,json,jwt
from util import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from sqlalchemy import desc
from autho.roles import roles
class User(db.Model):
    __tablename__ = "users"
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(30),nullable=False)
    email   = db.Column(db.String(30),unique=True,nullable=False)
    password= deferred(db.Column(db.String(255),nullable=False))
    role    = db.Column(db.String(30),nullable=False)
    active  = db.Column(db.Boolean,nullable=False)

    def __init__(self, name=None, email=None, password=None, role=None, active=True):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.active = active
        
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()
    
    def create(self,id=None,name="",email="",password="",role="",active=True):
        """Create a new user"""
        if role and role in roles:
            pass
        else:
            return jsonify({"message": "Invalid Role"}), 401
       
        if self.get_by_email(email):
            if id != None:
                self = self.get_by_id(id)
            else:
                return json.dumps({"success": False,"message":"User Already Exist"})
        self.name = name
        self.email=email
        if password:
            self.password=self.encrypt_password(password)
        elif id==None:
            return json.dumps({"success": False,"message":"Insert Password"})
            
        self.role=role
        self.active=active
        
        db.session.add(self) 
        try:
            db.session.commit()
            user = self
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return jsonify(success = True ,access_token=access_token, refresh_token=refresh_token,user_info = serialize(user,['password']))
        except:
            db.session.rollback()
            msg = {
                "error": "Error"
            }
            return json.dumps(msg) 
   
    def get_all(self,page,per_page,accounttype):
        """Get all users"""
        if self.query.filter_by(active=True).all():
            query = self.query
            query = query.order_by(User.name)
            query = query.filter_by(active=True)
            if accounttype != "All":
                query = query.filter_by(role=accounttype)
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            start_index = (page - 1) * per_page + 1
            end_index = min(paginated.total, page * per_page)
            users = [
                serialize(user,['password'])
                    for user in paginated.items
            ]
            results = {
                'users': users,
                'pagination': {
                    'count': paginated.total,
                    'page': page,
                    'per_page': per_page,
                    'pages': paginated.pages,
                    'from': start_index,
                    'to':   end_index
                }
            }
            
            return jsonify(results = results)
        return 0

    def get_by_email(self, email):
        """Get a user by email"""
        user = self.query.filter_by(email = email).one_or_none()
        if not user:
            return False
        return user
    def get_by_id(self,id):
        try:
            user = self.query.get(id)
            return user 
        except:
            return None
    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return jsonify("Wrong username or password"), 401
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return jsonify(access_token=access_token, refresh_token=refresh_token,user_info = serialize(user,['password']))
    
    def logout(self, jti, token_type="access"):
        """
        Logout user by adding the token's jti to the blacklist.
        """
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=token_type, created_at=now))  
        db.session.commit()
        return jsonify({"message": "Successfully logged out"}), 200
   
        


    
    