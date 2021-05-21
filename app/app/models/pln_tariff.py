from db import db
from datetime import datetime

class Pln_tariff(db.Model):
    __tablename__ = "pln_tariffs"

    id = db.Column(db.Integer, primary_key=True)
    pln_tariff_group = db.Column(db.String(100), nullable=True)
    pln_price = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # def update(self, pln_tariff_group, pln_price)
    #     timestamp = datetime.now().replace(microsecond=0)
    #     self.pln_tariff_group = pln_tariff_group
    #     self.pln_price = pln_price
    #     self.update_at = timestamp