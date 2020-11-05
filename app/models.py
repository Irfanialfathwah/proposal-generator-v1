from flask import request

from db import db
from app import app

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    role = db.Column(db.String(30))

    def __repr__(self):
        return f'<User {self.username}>'

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    email = db.Column(db.String(30))
    address = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)
    proposals = db.relationship('Proposal', back_populates="customer")

class Proposal(db.Model):
    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    location = db.Column(db.String(50))
    geocoordinates = db.Column(db.String(80))
    sketchup_model = db.Column(db.String(60))
    status = db.Column(db.String(20))
    customer = db.relationship("Parent", back_populates="proposals")
    roofs = db.relationship("Roof", backref="proposal")

    def __repr__(self):
        return f'<Proposal {self.customer}'

class Roof(db.Model):
    __tablename__ = "roofs"

    id = db.Column(db.Integer, primary_key= True)
    proposal_id = db.Column(db.String, db.ForeignKey('proposals.id'))
    pv_panel = db.Column(db.Integer)
    pv_panel_qty = db.Column(db.Integer)
    pv_mount = db.Column(db.Integer)
    pv_cable = db.Column(db.String(15))
    add_construction_qty = db.Column(db.Integer)
    add_construction_price = db.Column(db.Integer)
    azimuth = db.Column(db.Integer)
    angle = db.Column(db.Integer)
    solar_data = db.relationship("SolarYearData", backref='roof')

class SolarYearData(db.Model):
    __tablename__ = "solaryeardatas"

    id = db.Column(db.Integer, primary_key = True)
    roof_id = db.Column(db.Integer, db.ForeignKey('roofs.id'))
    monthly = db.relationship('SolarMonthData', backref="year")

class SolarMonthData(db.Model):
    __tablename__ = "solarmonthdatas"

    id = db.Column(db.Integer, primary_key = True)
    year_id = db.Column(db.Integer, db.ForeignKey('solaryeardatas.id'))
    month = db.Column(db.String(15))
    total = db.Column(db.Integer, nullable=True)
    hourly = db.relationship('SolarHourData', backref="month")

class SolarHourData(db.Model):
    __tablename__ = "solarhourdatas"

    id = db.Column(db.Integer, primary_key = True)
    month_id = db.Column(db.Integer, db.ForeignKey('solarmonthdatas.id'))
    hour = db.Column(db.Integer)