from dateutil.parser import parse

import vcr

from river_flows.clients.usgs_client import USGSClient
from river_flows.data.site_condition import SiteCondition

TEST_PATH = "tests/fixtures/unit/clients/usgs_client/"


@vcr.use_cassette(TEST_PATH + "test__current_flow__succcess.yaml")
def test__current_flow__success():
    # Arrange
    usgs_client = USGSClient()

    # Act
    site_condition = usgs_client.current_river_flow()

    # Assert
    expected_site_condition = SiteCondition(
        site_id="09067020",
        site_name="EAGLE R BLW WASTEWATER TREATMENT PLANT AT AVON, CO",
        timestamp=parse("2024-05-05T14:30:00.000-06:00"),
        value=516,
        unit="ft3/s",
    )

    assert site_condition == expected_site_condition


@vcr.use_cassette(TEST_PATH + "test__timeframe_river_flow__success.yaml")
def test__timeframe_river_flow__success():
    # Arrange
    usgs_client = USGSClient()
    start_date = parse("2024-05-01T00:00")
    end_date = parse("2024-05-02T00:00")

    # Act
    site_conditions = usgs_client.timeframe_river_flow(start_date=start_date, end_date=end_date)

    # Assert
    assert isinstance(site_conditions, list)
    assert len(site_conditions) == 97
    assert all(isinstance(site_condition, SiteCondition) for site_condition in site_conditions)
