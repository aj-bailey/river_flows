from datetime import datetime
from dateutil.parser import parse

import vcr

from river_flows.clients.usgs_client import USGSClient
from river_flows.data.site_condition import SiteCondition

@vcr.use_cassette('tests/fixtures/unit/clients/usgs_client/test__current_flow__succcess.yaml')
def test__current_flow__success():
    # Arrange
    usgs_client = USGSClient()
    
    # Act
    site_condition = usgs_client.current_river_flow()
    
    # Assert
    expected_site_condition = SiteCondition(
        site_id='09067020',
        site_name='EAGLE R BLW WASTEWATER TREATMENT PLANT AT AVON, CO',
        timestamp=parse("2024-05-05T14:30:00.000-06:00"),
        value=516,
        unit='ft3/s'
    )

    assert site_condition == expected_site_condition
