import pandas as pd
from config import ALLOWED_EXTENSIONS
from db import db
from app.models import SolarHourData, SolarMonthData, Roof

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_gsa_report_to_db(files):
    result = {}
    collection_data = []
    # print(files)
    for file in files:
        df = pd.read_excel(file, sheet_name=[4,5])
        # monthly_averages = df.get(4)[1:].reset_index(drop=True)
        hourly_profiles = df.get(5)[3:29].reset_index(drop=True)
        # monthly_averages.drop(index=1)
        # hourly_profiles.drop(index=1)
        # header1 = monthly_averages.iloc[0]
        header2 = hourly_profiles.iloc[0]

        # monthly_averages.columns = header1
        hourly_profiles.columns = header2

        # result_monthly = monthly_averages.to_dict('records')
        result_hourly = hourly_profiles.to_dict('splits')
        collection_data.append(result_hourly)
    yearly = []
    for data in collection_data:
        monthly = []
        for num,column in enumerate(data.get('columns')):
            # print(column)
            if type(column) is not float:
                solarmonth = SolarMonthData(month=column)
                row = 0
                for i in range(1,25):
                    energy_hour = data.get('data')[i][num]
                    if type(energy_hour) is not str:
                        row += energy_hour
                        solarhour = SolarHourData(month_id=solarmonth.id, energy=energy_hour, hour=i)
                        db.session.add(solarhour)
                        solarmonth.hourly.append(solarhour)
                solarmonth.energy = row
                db.session.add(solarmonth)
                monthly.append(solarmonth)
        yearly.append(monthly)
    # print(f'\n\n{yearly} {len(yearly)}')
    return yearly