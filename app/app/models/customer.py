from db import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(18), nullable=False)
    proposals = db.relationship('Proposal', backref="customer", cascade="all,delete")
    bids = db.relationship('Bid', backref="customer", cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def update(self, name, email, address, phone_number):
        timestamp = datetime.now().replace(microsecond=0)
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.updated_at = timestamp