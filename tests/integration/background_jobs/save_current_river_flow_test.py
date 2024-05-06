from dateutil.parser import parse

import vcr

from river_flows.background_jobs.save_current_river_flow import save_current_river_flow
from river_flows.data.site_condition import SiteCondition


VCR_DIR = 'tests/fixtures/integration/background_jobs/save_current_river_flow_test'

@vcr.use_cassette(f'{VCR_DIR}/test__save_current_river_flow__success.yaml')
def test__save_current_river_flow__success(initialize_and_clean_db):
    # Act
    site_condition = save_current_river_flow()
    
    # Assert
    expected_site_condition = SiteCondition(
        id=1,
        site_id='09067020',
        site_name='EAGLE R BLW WASTEWATER TREATMENT PLANT AT AVON, CO',
        timestamp=parse("2024-05-06T00:30:00.000+00"),
        value=521,
        unit='ft3/s'
    )

    assert site_condition == expected_site_condition
