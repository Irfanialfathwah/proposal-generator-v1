from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from config import (
        DATABASE,
        SECRET_KEY,
        DEBUG,
        CSRF_ENABLED,
        UPLOAD_IMAGES_FOLDER,
        UPLOAD_FILES_FOLDER,
        UPLOAD_PROPOSALS_FOLDER,
    )

app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = DATABASE.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config["DEBUG"] = DEBUG
app.config["CSRF_ENABLED"] = CSRF_ENABLED
app.config["UPLOAD_IMAGES_FOLDER"] = UPLOAD_IMAGES_FOLDER
app.config["UPLOAD_FILES_FOLDER"] = UPLOAD_FILES_FOLDER
app.config["UPLOAD_PROPOSALS_FOLDER"] = UPLOAD_PROPOSALS_FOLDER
# Load the views
import db
from app import views, models

