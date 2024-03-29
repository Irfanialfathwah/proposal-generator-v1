from db import db
from datetime import datetime

class Bid(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    number = db.Column(db.String(100), nullable=True)
    attachment = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def update(self, number, customer_id, proposal_id, attachment=None):
        timestamp = datetime.now().replace(microsecond=0)
        self.number = number
        self.customer_id = customer_id
        self.proposal_id = proposal_id
        if attachment is not None:
            self.attachment = attachment
        self.update_at = timestamp