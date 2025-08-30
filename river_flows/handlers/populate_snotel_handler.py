from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from river_flows.clients.snotel_client import SnotelAPIClient
from river_flows.data.snotel import BatchSnotel
from river_flows.repositories.snotel_repository import SnotelRepository


class PopulateSnotelHandler:
    def __init__(
        self, snotel_client: SnotelAPIClient, snotel_repository: SnotelRepository
    ):
        self.snotel_client = snotel_client
        self.snotel_repository = snotel_repository

    def handle(self, year: str, station_triplets: str):
        # Get snotel data from Snotel API
        begin_date = datetime.strptime(year, "%Y")
        end_date = begin_date + relativedelta(years=1) - timedelta(seconds=1)

        snotel_data = self.snotel_client.get_station_data(
            station_triplets=station_triplets, begin_date=begin_date, end_date=end_date
        )

        # Batch the snotel data for insertion
        batch_snotel = BatchSnotel(snotel_data=snotel_data)

        # Upsert data
        count_snotel_upserted = self.snotel_repository.upsert_records(
            records=batch_snotel
        )

        return count_snotel_upserted
