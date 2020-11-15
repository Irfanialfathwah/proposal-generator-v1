import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)
# Enable Flask's debugging features. Should be False in production
DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY')

UPLOAD_IMAGES_FOLDER = Path('.') / 'app' / 'static' / 'images' / 'sketchup-model'
UPLOAD_FILES_FOLDER = Path('.') / 'app' / 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls'}

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

DATABASE = {
    "SQLALCHEMY_DATABASE_URI" : os.getenv('DB_URL'),
    "SQLALCHEMY_TRACK_MODIFICATIONS" : True,
}