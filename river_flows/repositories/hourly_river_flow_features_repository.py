from sqlalchemy.orm import Session

from river_flows.repositories.base import AbstractRepository


class HourlyRiverFlowFeaturesRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def upsert_records(self, records) -> int:
        pass

    def get_records(self) -> list:
        pass
