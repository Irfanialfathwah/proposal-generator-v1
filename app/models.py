from db import db
from datetime import datetime
from app import app
import numpy as np

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100))
    email = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    # role = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

# class Role(db.Model):
#     __tablename__ = "roles"

#     id = db.Column(db.Integer, primary_key=True)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(18), nullable=False)
    proposals = db.relationship('Proposal', backref="customer", cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def update(self, name, email, address, phone_number):
        timestamp = datetime.now().replace(microsecond=0)
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.updated_at = timestamp

class Proposal(db.Model):
    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    date_of_proposals = db.Column(db.DateTime, nullable=False)
    num_of_roofs = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    geocoordinates = db.Column(db.String(80), nullable=False)
    sketchup_model = db.Column(db.String(100), nullable=True)
    pv_system_model = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    roofs = db.relationship("Roof", backref="proposal", cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Proposal {self.customer}'

    def update(self, customer_id, num_of_roofs, location, geocoordinates, sketchup_model=''):
        timestamp = datetime.now().replace(microsecond=0)
        self.customer_id = customer_id
        self.num_of_roofs = num_of_roofs
        self.location = location
        self.geocoordinates = geocoordinates
        self.sketchup_model = sketchup_model
        self.updated_at = timestamp

    def calculate_monthly_data(self):
        day_total = []
        yield_roof = []
        total_array_size = 0
        roof_data = []
        for roof in self.roofs:
            daily_sum = []
            yield_month = []
            daily_energy = []
            for index,solar_data in enumerate(roof.solar_data):
                total = 0
                total_with_array = 0
                for count,data in enumerate(solar_data.hourly):
                    total += data.energy
                daily_sum.append(total)
                daily_energy.append(total_with_array)
                yield_month.append(round(((total * roof.days_in_month[index])/1000) * roof.array_size,2))
            day_total.append(daily_sum)
            yield_roof.append(yield_month)
            total_array_size += roof.array_size
        # self.total_energy_perhour= [int(data) for data in list(map(sum, zip(*roof_data)))]
        self.day_total = day_total
        self.yield_roof = yield_roof
        self.yield_roof_total = [int(data) for data in list(map(sum, zip(*yield_roof)))]
        self.total_array_size = total_array_size

    @property
    def investment_payback_data(self):
        pv_system_investment = self.amount_after_tax / 1000000
        pln_price = 1550
        pln_price_incr = 5/100
        total_yield = self.total_yield
        pv_perf_decr = 0.8
        pv_perf = 100
        delta_harvest_new = 0-total_yield

        pv_investment_return = []
        list_yield_total = []
        list_pln_price = []
        list_harvest_value = []
        list_pv_perf = []

        for _ in range(25):
            list_yield_total.append(total_yield)
            list_pln_price.append(pln_price)
            harvest_value = round((total_yield * pln_price) / 1000,2)
            list_harvest_value.append(harvest_value)
            delta_harvest = delta_harvest_new + harvest_value
            delta_harvest_new = round(delta_harvest,2)
            pln_price = round((pln_price * pln_price_incr) + pln_price,2)
            pv_perf = round(pv_perf - pv_perf_decr,2)
            list_pv_perf.append(pv_perf)
            total_yield = round(total_yield * pv_perf/100,2)
            pv_investment_return.append(delta_harvest_new)

        return pv_investment_return, zip(list_yield_total, list_pln_price, list_harvest_value, pv_investment_return, list_pv_perf)


    @property
    def total_yield(self):
        return sum(self.yield_roof_total)/1000

    @property
    def total_energy_perhour(self):
        roof_data = [roof.energy_total_perhour for roof in self.roofs]
        return [data for data in list(map(sum, zip(*roof_data)))]

    @property
    def amount_before_tax(self):
        amount = 0
        for roof in self.roofs:
            amount += roof.total_amount
        return int(amount)

    @property
    def amount_tax(self):
        return int(self.amount_before_tax * 10/100)

    @property
    def amount_after_tax(self):
        return int(self.amount_before_tax + self.amount_tax)

class Roof(db.Model):
    __tablename__ = "roofs"

    id = db.Column(db.Integer, primary_key= True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    pv_panel = db.Column(db.Integer, nullable=True)
    pv_panel_qty = db.Column(db.Integer, nullable=True)
    pv_mount = db.Column(db.Integer, nullable=True)
    pv_cable = db.Column(db.Integer, nullable=True)
    add_construction_qty = db.Column(db.Integer, nullable=True)
    add_construction_price = db.Column(db.Integer, nullable=True)
    gsa_report_file = db.Column(db.String(50), nullable=True)
    azimuth = db.Column(db.Integer, nullable=False)
    angle = db.Column(db.Integer, nullable=False)
    solar_data = db.relationship("SolarMonthData", backref='roof', cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Roof {self.id}>'

    def update(self, pv_panel, pv_panel_qty, pv_cable, add_construction_qty, add_construction_price, azimuth, angle, gsa_report_file=''):
        timestamp = datetime.now().replace(microsecond=0)
        self.updated_at = timestamp
        self.pv_panel = pv_panel
        self.pv_panel_qty = pv_panel_qty
        self.pv_cable = pv_cable
        self.add_construction_qty = add_construction_qty
        self.add_construction_price = add_construction_price
        self.azimuth = azimuth
        self.angle = angle
        self.gsa_report_file = gsa_report_file

    @property
    def array_size(self):
        return self.pv_panel * self.pv_panel_qty / 1000

    @property
    def pv_panel_amount(self):
        return self.array_size * 9000000

    @property
    def add_construction_amount(self):
        return self.add_construction_qty * self.add_construction_price

    @property
    def pv_cable_amount(self):
        return self.pv_cable * 10000

    @property
    def total_amount(self):
        return int(self.pv_panel_amount + self.add_construction_amount + self.pv_cable_amount)

    @property
    def price_perunit(self):
        return int(self.total_amount/self.array_size)

    @property
    def days_in_month(self):
        return [31,29,31,30,31,30,31,31,30,31,30,31]

    @property
    def energy_total_perhour(self):
        hour_data = [np.array([0 for _ in range(24)]) for _i in range(12)]
        for index,month in enumerate(self.solar_data):
            for count,hour in enumerate(month.hourly):
                hour_data[index][count] += hour.energy
        return hour_data

class SolarMonthData(db.Model):
    __tablename__ = "solarmonthdatas"

    id = db.Column(db.Integer, primary_key = True)
    roof_id = db.Column(db.Integer, db.ForeignKey('roofs.id'))
    month = db.Column(db.String(15))
    energy_perday = db.Column(db.Integer, nullable=True)
    energy = db.Column(db.Integer)
    hourly = db.relationship('SolarHourData', backref="month", cascade="all,delete")

    def __repr__(self):
        return f'<SolarMonthData {self.month}>'

class SolarHourData(db.Model):
    __tablename__ = "solarhourdatas"

    id = db.Column(db.Integer, primary_key = True)
    month_id = db.Column(db.Integer, db.ForeignKey('solarmonthdatas.id'))
    hour = db.Column(db.Integer)
    energy = db.Column(db.Integer)

    def __repr__(self):
        return f'<SolarHourData {self.energy}>'