from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests

class SnotelAPIClient():
    def __init__(self):
        self.base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"
    
    def get_station_data(
        self,
        station_triplets: str,
        begin_date:       str,
        end_date:         str = None,
        elements:         str = "*",
        duration:         str = "HOURLY",
    ):
        begin_date = datetime.strptime(begin_date, "%Y-%m-%d")

        if not end_date:
            end_date = begin_date + relativedelta(years=1) - relativedelta(days=1)

        params = {
            "stationTriplets": station_triplets,
            "beginDate": begin_date,
            "endDate": end_date,
            "elements": elements,
            "duration": duration 
        }

        response = requests.get(self.base_url + "/data?", params=params)

        if response.status_code == 200:
            return response.json()[0]
        else:
            raise Exception(
                f"Failed to fetch data for {begin_date} - {end_date} {station_triplets}: {response.status_code} - {response.text}"
            )

