from datetime import datetime
from typing import Optional

from river_flows.config.config import USGS_EWRSD_SITE
from river_flows.data.site_condition import SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository


class SiteConditionsHandler:
    def __init__(self, site_condition_repo: SiteConditionRepository):
        self.site_condition_repo = site_condition_repo

    def handle(self, start_date: str, end_date: str, site_id: Optional[str]) -> list[SiteCondition]:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        if not site_id:
            site_id = USGS_EWRSD_SITE

        site_conditions = self.site_condition_repo.get_records(
            start_date=start_datetime, end_date=end_datetime, site_id=site_id
        )
        return site_conditions
