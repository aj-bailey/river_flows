from datetime import datetime, timedelta
from dateutil.parser import parse

import vcr

from river_flows.clients.usgs_client import USGSClient
from river_flows.data.site_condition import BatchSiteConditions, SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.utils.db import get_session

VCR_DIR = "tests/fixtures/integration/background_jobs/save_previous_date_river_flows"


@vcr.use_cassette(f"{VCR_DIR}/test__save_previous_date_river_flows__success.yaml")
def save_previous_date_river_flows() -> SiteCondition:
    usgs_client = USGSClient()
    site_condition_repo = SiteConditionRepository(get_session())
    start_date, end_date = _get_previous_date_start_end()

    previous_date_river_flows = usgs_client.timeframe_river_flow(
        start_date=start_date, end_date=end_date
    )
    site_conditions = BatchSiteConditions(site_conditions=previous_date_river_flows)

    site_conditions_count = site_condition_repo.upsert_records(site_conditions)

    return site_conditions_count


def _get_previous_date_start_end() -> tuple[datetime, datetime]:
    previous_date = (datetime.now() - timedelta(days=1)).date()
    previous_date_start = parse(str(previous_date))
    previous_date_end = previous_date_start + timedelta(minutes=1439)

    return previous_date_start, previous_date_end
