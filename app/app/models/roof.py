from db import db
from datetime import datetime
import numpy as np

class Roof(db.Model):
    __tablename__ = "roofs"

    id = db.Column(db.Integer, primary_key= True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    pv_panel = db.Column(db.Integer, nullable=True)
    pv_panel_qty = db.Column(db.Integer, nullable=True)
    pv_mount = db.Column(db.Integer, nullable=True)
    pv_cable = db.Column(db.Integer, nullable=True)
    add_construction_qty = db.Column(db.Integer, nullable=True)
    add_construction_price = db.Column(db.String(100), nullable=True)
    gsa_report_file = db.Column(db.String(100), nullable=True)
    azimuth = db.Column(db.Integer, nullable=False)
    angle = db.Column(db.Integer, nullable=False)
    solar_data = db.relationship("SolarMonthData", backref='roof', cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Roof {self.id}>'

    def update(self, pv_panel, pv_panel_qty, pv_cable, add_construction_qty, add_construction_price, azimuth, angle, gsa_report_file=None):
        timestamp = datetime.now().replace(microsecond=0)
        self.updated_at = timestamp
        self.pv_panel = pv_panel
        self.pv_panel_qty = pv_panel_qty
        self.pv_cable = pv_cable
        self.add_construction_qty = add_construction_qty
        self.add_construction_price = add_construction_price
        self.azimuth = azimuth
        self.angle = angle
        if gsa_report_file is not None:
            self.gsa_report_file = gsa_report_file

    @property
    def roof_yearly_yield(self):
        # daily_sum = []
        yield_month = []
        # daily_energy = []
        for index,solar_data in enumerate(self.solar_data):
            total = 0
            # total_with_array = 0
            # for count,data in enumerate(solar_data.hourly):
            #     total += data.energy
            # daily_sum.append(total)
            # daily_energy.append(total_with_array)
            yield_month.append(round(((solar_data.energy * self.days_in_month[index])/1000) * self.array_size,1))
        return yield_month

    @property
    def total_roof_yearly_yield(self):
        return sum(self.roof_yearly_yield)

    @property
    def avg_daily_harvest(self):
        return (self.total_roof_yearly_yield/365)

    @property
    def kwh_kwp_day(self):
        return round(self.avg_daily_harvest/self.array_size,1)

    @property
    def array_size(self):
        return self.pv_panel * self.pv_panel_qty / 1000

    @property
    def pv_panel_amount(self):
        return self.array_size * 11137038

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
