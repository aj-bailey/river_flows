from datetime import datetime, timezone

from river_flows.data.site_condition import SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository


def test__create_site_condition__success(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    test_dt = datetime(year=2024, month=5, day=5, hour=7, minute=30, second=0, tzinfo=timezone.utc)
    site_condition = SiteCondition(**{"site_id": "TEST_ID", "site_name": "TEST_NAME", "timestamp": test_dt, "value": 1, "unit": "ft3/s"})
    site_condition_repository = SiteConditionRepository(session=session)
    
    # Act
    inserted_site_condition = site_condition_repository.create_record(site_condition)

    # Assert
    expected_site_condition = SiteCondition(id=1, site_id="TEST_ID", site_name="TEST_NAME", timestamp=test_dt, value=1, unit='ft3/s')

    assert inserted_site_condition == expected_site_condition
