from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from config import (
        DATABASE,
        SECRET_KEY,
        DEBUG,
        CSRF_ENABLED
    )

print(SECRET_KEY)
print(DATABASE)

app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = DATABASE.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config["DEBUG"] = DEBUG
app.config["CSRF_ENABLED"] = CSRF_ENABLED
# Load the views
import db
from app import views, models

