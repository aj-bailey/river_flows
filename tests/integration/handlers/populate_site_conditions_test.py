import vcr

from river_flows.clients.usgs_client import USGSClient
from river_flows.handlers.populate_site_conditions_handler import PopulateSiteConditionsHandler
from river_flows.repositories.site_condition_repository import SiteConditionRepository


TEST_PATH = 'tests/fixtures/integration/handlers/populate_site_conditions/'


@vcr.use_cassette(TEST_PATH + 'test__handle__success.yaml')
def test__handle__success(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    usgs_client = USGSClient()
    site_condition_repo = SiteConditionRepository(session)
    handler = PopulateSiteConditionsHandler(usgs_client=usgs_client, site_condition_repo=site_condition_repo)
    
    # Act
    count_site_conditions_upserted = handler.handle(start_date="05-01-2024", end_date="05-02-2024")

    # Assert
    assert count_site_conditions_upserted == 96
