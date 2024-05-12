from datetime import timedelta
from dateutil.parser import parse

from river_flows.clients.usgs_client import USGSClient
from river_flows.data.site_condition import BatchSiteConditions, SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository

class PopulateSiteConditionsHandler():
    def __init__(self, usgs_client: USGSClient, site_condition_repo: SiteConditionRepository):
        self.usgs_client = usgs_client
        self.site_condition_repo = site_condition_repo

    def handle(self, start_date, end_date):
        # Get site conditions from USGS API
        start_datetime = parse(start_date)
        end_datetime = parse(end_date) - timedelta(seconds=1)
        site_conditions = self.usgs_client.timeframe_river_flow(start_date=start_datetime, end_date=end_datetime)

        # Batch the individual site conditions for insertion
        batch_site_conditions = BatchSiteConditions(site_conditions=site_conditions)

        # Store site conditions in database
        count_conditions_upserted = self.site_condition_repo.upsert_records(batch_site_conditions)

        return count_conditions_upserted
