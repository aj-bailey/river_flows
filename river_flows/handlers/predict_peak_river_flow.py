from datetime import datetime


class PredictPeakRiverFlowHandler:
    def __init__(self, sc_repo, snotel_repo):
        self.sc_repo = sc_repo
        self.snotel_repo = snotel_repo

    def handle(self):
        trips = ["1040:CO:SNTL", "842:CO:SNTL", "485:CO:SNTL"]
        ids = ["09070000", "09067020", "09065500"]

        year = 2004
        start_dt = datetime.strptime(str(year), "%Y")
        end_dt = datetime.strptime(str(year + 1), "%Y")

        data = self.snotel_repo.get_records(start_date=start_dt, end_date=end_dt, station_triplets=trips[2])

        return data
