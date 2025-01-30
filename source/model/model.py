import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import deferred
from flask_jwt_extended import JWTManager
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from datetime import datetime
from MySQLdb import IntegrityError
from flask import jsonify
import json

db = SQLAlchemy()
jwt = JWTManager()



class BaseModel(db.Model):
    __abstract__ = True  

    def save(self):
        """Save the instance to the database with enhanced error handling."""
        db.session.add(self)
        try:
            db.session.commit()
            return self  
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Integrity violation occurred.")  
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError("Database error occurred.")  
        except Exception as e:
            db.session.rollback()
            raise ValueError("An unexpected error occurred.")  


  