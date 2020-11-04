from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views
import db

from config import DATABASE

app.config.update(DATABASE)
# Load the config file
app.config.from_object('config')
app.secret_key = "my precious"

