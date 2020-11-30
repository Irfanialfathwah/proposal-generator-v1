from db import db

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