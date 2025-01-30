from flask import Flask
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_cors import CORS
from dotenv import load_dotenv
from os.path import join, dirname
import os
import jwt
# Import project modules
from middleware.checkdata import reject_unsanitized_data
from errorHandlers import errorhandlers
from controllers import controllers
from model import *

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
load_dotenv(verbose=True)

# Initialize Flask app
app = Flask(
    __name__,
    static_folder="build",
    template_folder="build",
    static_url_path=""
)
CORS(app)
# Load configuration from environment variable
app.config.from_object(os.environ.get("ENV_KEY"))

# Set up SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@"
    f"{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"
)

# Middleware and extensions
app.before_request(reject_unsanitized_data)
db.init_app(app)
jwt.init_app(app)
errorhandlers.init_app(app)

# Migrations
migrate = Migrate(app, db, compare_type=True)

# Initialize Flask-Seeder
seeder = FlaskSeeder()
seeder.init_app(app, db)

# Initialize controllers
controllers.init_app(app)

# Main entry point
if __name__ == '__main__':
    app.run()

