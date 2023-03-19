from db import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    std_price = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(100), nullable=True)
    brochure = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    proposals = db.relationship("Proposal", secondary="proposal_products", cascade="all,delete")

    def update(self, product_name, std_price, unit, brochure=None):
        timestamp = datetime.now().replace(microsecond=0)
        self.product_name = product_name
        self.std_price = std_price
        self.unit = unit
        if brochure is not None:
            self.brochure = brochure
        self.updated_at = timestamp


class Qty_product(db.Model):
    __tablename__ = "qty_products"

    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    qty = db.Column(db.Integer, nullable=True)
    products = db.relationship('Product', backref="qty_product")
    proposals = db.relationship('Proposal', backref="qty_product")