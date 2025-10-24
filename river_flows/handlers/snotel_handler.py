from datetime import datetime

from river_flows.data.snotel import Snotel
from river_flows.repositories.snotel_repository import SnotelRepository


class SnotelHandler:
    def __init__(self, snotel_repo: SnotelRepository):
        self.snotel_repo = snotel_repo

    def handle(self, start_date: str, end_date: str, station_triplets: str) -> list[Snotel]:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        snotel_data = self.snotel_repo.get_records(
            start_date=start_datetime,
            end_date=end_datetime,
            station_triplets=station_triplets,
        )

        return snotel_data
