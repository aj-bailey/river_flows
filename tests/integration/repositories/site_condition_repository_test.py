from datetime import datetime, timezone

import pytest

from river_flows.data.site_condition import SiteCondition
from river_flows.repositories.site_condition_repository import SiteConditionRepository


def test__create_site_condition__success(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    test_dt = datetime(
        year=2024, month=5, day=5, hour=7, minute=30, second=0, tzinfo=timezone.utc
    )
    site_condition = SiteCondition(
        **{
            "site_id": "TEST_ID",
            "site_name": "TEST_NAME",
            "timestamp": test_dt,
            "value": 1,
            "unit": "ft3/s",
        }
    )
    site_condition_repository = SiteConditionRepository(session=session)

    # Act
    inserted_site_condition = site_condition_repository.create_record(site_condition)

    # Assert
    expected_site_condition = SiteCondition(
        site_id="TEST_ID",
        site_name="TEST_NAME",
        timestamp=test_dt,
        value=1,
        unit="ft3/s",
    )

    assert inserted_site_condition == expected_site_condition


@pytest.mark.parametrize("seed_site_conditions", [10], indirect=True)
def test__get_site_conditions__success(initialize_and_clean_db, seed_site_conditions):
    # Arrange
    session = initialize_and_clean_db
    site_condition_repository = SiteConditionRepository(session=session)

    # Act
    records = site_condition_repository.get_records(
        start_date="2024-01-01", end_date="2024-01-02", site_id="TEST_ID"
    )

    # Assert
    assert len(records) == 10
    assert all(isinstance(record, SiteCondition) for record in records)
