# Enable Flask's debugging features. Should be False in production
DEBUG = True

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

DATABASE = {
    "SQLALCHEMY_DATABASE_URI" : "postgresql://postgres:admin@localhost:5432/proposal_generator",
    "SQLALCHEMY_TRACK_MODIFICATIONS" : True,
}