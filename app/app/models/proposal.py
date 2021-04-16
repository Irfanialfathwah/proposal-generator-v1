from db import db
from datetime import datetime
# import numpy as np

class Proposal(db.Model):
    __tablename__ = "proposals"

    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    date_of_proposals = db.Column(db.DateTime, nullable=False)
    project_name = db.Column(db.String(100), nullable=True)
    num_of_roofs = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    geocoordinates = db.Column(db.String(100), nullable=True)
    sketchup_model = db.Column(db.String(100), nullable=True)
    pv_system_model = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    inverter_stg3 = db.Column(db.Integer, nullable=True)
    inverter_stg6 = db.Column(db.Integer, nullable=True)
    inverter_stg20 = db.Column(db.Integer, nullable=True)
    # inverter_stg125 = db.Column(db.Integer, nullable=True)
    energy_accounting_system = db.Column(db.Integer, nullable=True)
    transport_price = db.Column(db.Integer, nullable=True)
    installation_price = db.Column(db.Integer, nullable=True)
    roofs = db.relationship("Roof", backref="proposal", cascade="all,delete")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    discount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Proposal {self.customer}'

    def update(self, customer_id, project_name, num_of_roofs, sketchup_model=None ):
        timestamp = datetime.now().replace(microsecond=0)
        self.customer_id = customer_id
        self.project_name = project_name
        self.num_of_roofs = num_of_roofs
        if sketchup_model is not None:
            self.sketchup_model = sketchup_model
        # self.inverter_stg3 = inverter_stg3
        # self.inverter_stg6 = inverter_stg6
        # self.inverter_stg20 = inverter_stg20
        # self.energy_accounting_system = energy_accounting_system
        # self.transport_price = transport_price
        # self.installation_price = installation_price
        self.updated_at = timestamp
        #, inverter_stg3, inverter_stg6, inverter_stg20, energy_accounting_system, transport_price, installation_price
        
    def update_quotation(self, id, inverter_stg3, inverter_stg6, inverter_stg20, energy_accounting_system, transport_price, installation_price, discount):
        timestamp = datetime.now().replace(microsecond=0)
        self.updated_at = timestamp
        self.id = id
        self.inverter_stg3 = inverter_stg3
        self.inverter_stg6 = inverter_stg6
        self.inverter_stg20 = inverter_stg20
        # self.inverter_stg125 = inverter_stg125
        self.energy_accounting_system = energy_accounting_system
        self.transport_price = transport_price
        self.installation_price = installation_price
        self.discount = discount
        
    def calculate_monthly_data(self):
        # day_total = []
        yield_roof = []
        roof_data = []
        for roof in self.roofs:
            # daily_sum = []
            # yield_month = []
            # daily_energy = []
            # for index,solar_data in enumerate(roof.solar_data):
            #     total = 0
            #     total_with_array = 0
            #     for count,data in enumerate(solar_data.hourly):
            #         total += data.energy
            #     daily_sum.append(total)
            #     daily_energy.append(total_with_array)
            #     yield_month.append(round(((total * roof.days_in_month[index])/1000) * roof.array_size,2))
            # # day_total.append(daily_sum)
            yield_roof.append(roof.roof_yearly_yield)
        # self.total_energy_perhour= [int(data) for data in list(map(sum, zip(*roof_data)))]
        # self.day_total = day_total
        self.yield_roof = yield_roof
        self.yield_roof_total = [int(data) for data in list(map(sum, zip(*yield_roof)))]

    @property
    def total_avg_daily_harvest(self):
        total = 0
        for roof in self.roofs:
            total += roof.avg_daily_harvest
        return total

    @property
    def avg_kwh_kwp_day(self):
        total = 0
        for roof in self.roofs:
            total += roof.kwh_kwp_day
        return round(total / self.num_of_roofs,2)

    @property
    def total_array_size(self):
        total = 0
        for roof in self.roofs:
            total += roof.array_size
        return total

    @property
    def total_panel_qty(self):
        total = 0
        for roof in self.roofs:
            total += roof.pv_panel_qty
        return total

    @property
    def investment_payback_data(self):
        pv_system_investment = self.amount_after_tax / 1000000
        pln_price = 1550
        pln_price_incr = 5/100
        static_total_yield = self.total_yield
        total_yield = self.total_yield
        pv_perf_decr = 0.8
        pv_perf = 100
        delta_harvest_new = pv_system_investment * -1
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
            # print(delta_harvest)
            delta_harvest_new = round(delta_harvest,2)
            pln_price = int((pln_price * pln_price_incr) + pln_price)
            pv_perf = round(pv_perf - pv_perf_decr,2)
            list_pv_perf.append(pv_perf)
            total_yield = round(static_total_yield * pv_perf/100,2)
            pv_investment_return.append(delta_harvest_new)
        self._end_pv_investment_return = pv_investment_return[-1]
        pv_graph_investment = self._compress_year(pv_investment_return)
        list_yield_total = self._compress_year(list_yield_total)
        list_pln_price = self._compress_end_val(list_pln_price)
        list_harvest_value = self._compress_year(list_harvest_value)
        list_pv_perf = self._compress_end_val(list_pv_perf)
        return pv_investment_return, zip(list_yield_total, list_pln_price, list_harvest_value, pv_graph_investment, list_pv_perf)


    def _compress_end_val(self,value):
        value_new = value[:10]
        value_new.append(value[14])
        value_new.append(value[19])
        value_new.append(value[-1])
        return value_new

    def _compress_year(self,value):
        list_val = value[:10]
        list_val.append(sum(value[10:15]))
        list_val.append(sum(value[15:20]))
        list_val.append(sum(value[20:]))
        return list_val

    @property
    def roof_performance_result(self):
        list_kwh_kwp_day = [roof.kwh_kwp_day for roof in self.roofs]
        result = [int((roof.kwh_kwp_day - max(list_kwh_kwp_day))/min(list_kwh_kwp_day) * 100) for roof in self.roofs]
        return ["Best" if r == 0 else r for r in result]

    @property
    def end_pv_investment_return(self):
        return self._end_pv_investment_return

    @property
    def total_yield(self):
        return sum(self.yield_roof_total)/1000

    @property
    def total_energy_perhour(self):
        roof_data = [roof.energy_total_perhour for roof in self.roofs]
        return [data for data in list(map(sum, zip(*roof_data)))]

    @property
    def inverter_stg3_amount(self):
        return self.inverter_stg3 * 5700000

    @property
    def inverter_stg6_amount(self):
        return self.inverter_stg6 * 14500000

    @property
    def inverter_stg20_amount(self):
        return self.inverter_stg20 * 174000000

    # @property
    # def inverter_stg125_amount(self):
    #     return self.inverter_stg125 * 174000000

    @property
    def eas_amount(self):
        return self.energy_accounting_system * 5000000

    @property
    def amount_before_tax(self):
        amount = 0
        for roof in self.roofs:
            amount += roof.total_amount
        return int(amount + self.inverter_stg3_amount + self.inverter_stg6_amount + self.inverter_stg20_amount + self.eas_amount + self.transport_price + self.installation_price)

    @property
    def amount_tax(self):
        return int(self.amount_after_discount * 10/100)

    @property
    def amount_after_tax(self):
        return int(self.amount_after_discount + self.amount_tax)

    @property
    def amount_after_discount(self):
        return int(self.amount_before_tax - self.discount)