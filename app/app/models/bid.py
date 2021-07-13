from db import db
from datetime import datetime

class Bid(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100), nullable=True)
    attachment = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    proposals = db.relationship('Proposal', backref="bid", cascade="all,delete")

    def update(self, number, attachment=None):
        timestamp = datetime.now().replace(microsecond=0)
        self.number = number
        if attachment is not None:
            self.attachment = attachment
        self.update_at = timestamp