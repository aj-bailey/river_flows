from datetime import datetime
from functools import reduce

import numpy as np
import pandas as pd
import requests

from river_flows.data.snotel import Snotel


class SnotelAPIClient:
    def __init__(self):
        self.base_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"

    def get_station_data(
        self,
        station_triplets: str,
        begin_date: datetime,
        end_date: datetime,
        elements: str = "PREC, SNWD, TOBS, WTEQ",
        duration: str = "DAILY",
    ):
        params = {
            "stationTriplets": station_triplets,
            "beginDate": begin_date,
            "endDate": end_date,
            "elements": elements,
            "duration": duration,
        }

        response = requests.get(self.base_url + "/data?", params=params)

        if response.status_code == 200:
            parsed_response = self._parse_station_data(response.json())
            return parsed_response
        else:
            raise Exception(
                f"Failed to fetch data for {begin_date} - {end_date} {station_triplets}: {response.status_code} - {response.text}"
            )

    def _parse_station_data(self, station_data: dict) -> list[Snotel]:
        data = station_data[0]
        station_triplet = data["stationTriplet"]

        element_dfs = []

        for element_data in data["data"]:
            element_name = element_data["stationElement"]["elementCode"]
            df = pd.DataFrame(element_data["values"]).rename(columns={"value": element_name.lower()})
            element_dfs.append(df)

        dfs_merged = reduce(lambda df1, df2: pd.merge(df1, df2, on="date", how="outer"), element_dfs)
        dfs_merged = dfs_merged.rename(columns={"date": "timestamp"})
        dfs_merged["station_triplets"] = station_triplet

        # Clean NaN values
        dfs_cleaned = dfs_merged.replace({np.inf: None, -np.inf: None, np.nan: None, "NaN": None})

        data_dict = dfs_cleaned.to_dict(orient="records")
        snotel_data = [Snotel.model_validate(data) for data in data_dict]

        return snotel_data
