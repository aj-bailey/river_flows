from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests

import pandas as pd


class SnotelAPIClient:
    def __init__(self):
        self.base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"

    def fetch_station_data(
        self,
        station_triplets: str,
        begin_date: str,
        end_date: str = None,
        elements: str = "*",
        duration: str = "HOURLY",
    ):
        begin_date = datetime.strptime(begin_date, "%Y-%m-%d")

        if not end_date:
            end_date = begin_date + relativedelta(years=1) - relativedelta(days=1)
        params = {
            "stationTriplets": station_triplets,
            "beginDate": begin_date,
            "endDate": end_date,
            "elements": elements,
            "duration": duration,
        }

        response = requests.get(self.base_url + "/data?", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch data for {begin_date} - {end_date} {station_triplets}: {response.status_code} - {response.text}"
            )


stations_base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/stations"
station_data_base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data"
station_data_base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data?stationTriplets=485%3ACO%3ASNTL%2C%201040%3ACO%3ASNTL%2C%20842%3ACO%3ASNTL&elements=%2A&duration=DAILY&beginDate=2024-01-01&periodRef=END&centralTendencyType=NONE&returnFlags=false&returnOriginalValues=false&returnSuspectData=false"

# ids = ['09009040', '1040', '842', '485']
# df = df[df['stationId'].isin(ids)]
# data_df = pd.DataFrame()

# for i, station in df.iterrows():
#     for element in station['data']:
#         temp_df = pd.DataFrame(element['values'])
#         import ipdb; ipdb.set_trace()


# fremont pass: 485:CO:SNTL
# Vail Mtn: 842:CO:SNTL
# McCoy Park: 1040:CO:SNTL

if __name__ == "__main__":
    station_triplets = ["485:CO:SNTL", "842:CO:SNTL", "1040:CO:SNTL"]
    start_year = 2000
    dates = [datetime(year, 1, 1) for year in range(start_year, datetime.now().year)]
    target_element_codes = [
        "PREC",
        "SNWD",
        "TOBS",
        "WTEQ",
    ]
    year_dfs = []
    client = SnotelAPIClient()

    # for date in dates:
    try:
        data = client.fetch_station_data(
            station_triplets=station_triplets[0],
            begin_date="2007-01-01",
            end_date="2011-01-01",
        )
    except Exception:
        print(f"Failed to fetch data for {str(date.date())} {station_triplets[0]}")
        # continue

    element_dfs = []
    for e_data in data[0]["data"]:
        element_code = e_data["stationElement"]["elementCode"]

        if element_code not in target_element_codes:
            continue

        element_df = pd.DataFrame(data=e_data["values"])
        element_df.rename(
            columns={"value": element_code, "date": "timestamp_local"}, inplace=True
        )
        element_df["timestamp_local"] = pd.to_datetime(element_df["timestamp_local"])
        element_dfs.append(element_df)

    # Merge element dataframes
    merged_df = element_dfs[0]
    for element_df in element_dfs[1:]:
        merged_df = pd.merge(merged_df, element_df, on="timestamp_local", how="outer")
    merged_df.sort_values(by="timestamp_local", inplace=True)
    merged_df["station_triplet"] = "485:CO:SNTL"
    df = pd.DataFrame()
    df = pd.concat([df, merged_df], axis=1)

    year_dfs.append(df)
    # import ipdb; ipdb.set_trace()

    import ipdb

    ipdb.set_trace()
