from db import db

class Proposal_product(db.Model):
    __tablename__ = "proposal_products"

    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal_id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_id'), primary_key = True)