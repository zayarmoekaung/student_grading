from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_DB    =   ''
    SECRET_KEY = 'secret'
    JWT_SECRET_KEY = ''
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    UPLOAD_FOLDER = 'documents/'
    MAIL_SERVER=""
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    pass

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB    =   'grading'
    SECRET_KEY = 'secret'
    JWT_SECRET_KEY = '704576398d9c1cd89a16cd7955ac3b8e'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    UPLOAD_FOLDER = 'documents/'
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
