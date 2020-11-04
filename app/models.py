from flask import request

from db import db
from app import app


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Proposal(db.Model):
    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(40))
    number_of_roof = db.Column(db.Integer)
    geocoordinate = db.Column(db.String(100))
    status = db.Column(db.String(30))

    def __repr__(self):
        return f'<Proposal {self.customer}'