import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)
# Enable Flask's debugging features. Should be False in production
DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY')

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

DATABASE = {
    "SQLALCHEMY_DATABASE_URI" : os.getenv('DB_URL'),
    "SQLALCHEMY_TRACK_MODIFICATIONS" : True,
}