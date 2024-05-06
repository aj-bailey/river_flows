from river_flows.clients.usgs_client import USGSClient
from river_flows.data.site_condition import SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.utils.db import get_session

def save_current_river_flow() -> SiteCondition:
    usgs_client = USGSClient()
    site_condition_repo = SiteConditionRepository(get_session())

    current_river_flow = usgs_client.current_river_flow()
    site_condition = site_condition_repo.create_record(current_river_flow)

    print(f"Record created: {site_condition_repo}")

    return site_condition
