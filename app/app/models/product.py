from db import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    std_price = db.Column(db.Integer, nullable=True)
    brochure = db.Column(db.String(100), nullable=True)
    proposals = db.relationship('Proposal', backref="product", cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def update(self, product_name, std_price, brochure=None):
        timestamp = datetime.now().replace(microsecond=0)
        self.product_name = product_name
        self.std_price = std_price
        if brochure is not None:
            self.brochure = brochure
        self.updated_at = timestamp