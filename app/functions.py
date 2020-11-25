import pandas as pd
import re
from config import ALLOWED_EXTENSIONS
from db import db
from app.models import SolarHourData, SolarMonthData, Roof

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_gsa_report_to_db(files):
    result = {}
    collection_data = []
    proposal_data = {}
    roof_data = []
    # print(files)
    for file in files:
        df = pd.read_excel(file, sheet_name=[1,2,4,5])
        pv_config = df.get(2).reset_index(drop=True)
        sites_info = df.get(1).reset_index(drop=True)
        hourly_profiles = df.get(5)[3:29].reset_index(drop=True)
        pv_system_model = pv_config.iloc[1][0]
        tilt = int(pv_config.iloc[4][1])
        azimuth = int(pv_config.iloc[5][1])
        print(tilt)
        print(azimuth)
        print(pv_config)
        print(pv_system_model)
        roof_data.append({'azimuth' : azimuth, 'angle': tilt})
        comp = re.compile(r'^[^\(]+')
        geocoordinates = re.match(comp, sites_info.iloc[1][1]).group().replace(',', '').replace(' ', '')
        location = sites_info.iloc[0][1]
        print(location)
        print(geocoordinates)
        proposal_data.update({
            'geocoordinates' : geocoordinates,
            'pv_system_model' : pv_system_model
        })
        nan = ['nan', 'Nan', 'NaN', 'NAN']
        if location not in nan:
            proposal_data.update({
                'location':location
            })
        header2 = hourly_profiles.iloc[0]
        hourly_profiles.columns = header2
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
    proposal_data.update({
        'roofs': roof_data
    })
    # print(f'\n\n{yearly} {len(yearly)}')
    return yearly, proposal_data