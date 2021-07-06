from db import db

class Proposal_product(db.Model):
    __tablename__ = "proposal_products"

    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)