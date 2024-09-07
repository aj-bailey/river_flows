from river_flows.clients.usgs_client import USGSClient
from river_flows.repositories.site_condition_repository import SiteConditionRepository

class SiteConditionsHandler():
    def __init__(self, usgs_client: USGSClient, site_condition_repo: SiteConditionRepository):
        self.usgs_client = usgs_client
        self.site_condition_repo = site_condition_repo
