from datetime import datetime, timezone

import pytest

from river_flows.data.site_condition import SiteCondition
from river_flows.handlers.site_conditions_handler import SiteConditionsHandler
from river_flows.orm.site_condition import SiteCondition as SiteConditionORM
from river_flows.repositories.site_condition_repository import SiteConditionRepository


@pytest.mark.parametrize('seed_site_conditions', [10], indirect=True)
def test__handle__success_records(initialize_and_clean_db, seed_site_conditions):
    # Arrange
    session = initialize_and_clean_db
    site_condition_repo = SiteConditionRepository(session=session)
    site_conditions_handler = SiteConditionsHandler(site_condition_repo=site_condition_repo)

    # Act
    records = site_conditions_handler.handle(start_date='2024-01-01', end_date='2024-01-02', site_id='TEST_ID')
    
    # Assert
    assert len(records) == 10
    assert all(isinstance(record, SiteCondition) for record in records)

def test__handle__success_no_records(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    site_condition_repo = SiteConditionRepository(session=session)
    site_conditions_handler = SiteConditionsHandler(site_condition_repo=site_condition_repo)


    # Act
    records = site_conditions_handler.handle(start_date='2024-01-01', end_date='2024-01-02', site_id='TEST_ID')
    
    # Assert
    assert records == []

def test__handle__success_no_site_id(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    site_condition_repo = SiteConditionRepository(session=session)
    site_condition_handler = SiteConditionsHandler(site_condition_repo=site_condition_repo)

    site_condition = SiteConditionORM(
            site_id='09067020',
            site_name="TEST_NAME",
            timestamp=datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc),
            value=100,
            unit="ft3/s"
        )
    session.add(site_condition)
    session.commit()

    # Act
    records = site_condition_handler.handle(start_date='2024-01-01', end_date='2024-01-02', site_id=None)

    # Assert
    assert records[0].site_id == '09067020'

@pytest.mark.parametrize('seed_site_conditions', [10], indirect=True)
def test__handle__bad_dates(initialize_and_clean_db, seed_site_conditions):
    # Arrange
    session = initialize_and_clean_db
    site_condition_repo = SiteConditionRepository(session=session)
    site_conditions_handler = SiteConditionsHandler(site_condition_repo=site_condition_repo)

    # Act
    records = site_conditions_handler.handle(start_date='2024-01-02', end_date='2024-01-01', site_id='TEST_ID')
    
    # Assert
    assert records == []
