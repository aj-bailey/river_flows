from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine

from river_flows.orm.site_condition import SiteCondition as SiteConditionORM
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.utils.db import TransactionalSession
from tests.utils.db import clean_database


@pytest.fixture
def db_engine():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/river_flows-test"
    )

    return engine


@pytest.fixture
def initialize_and_clean_db():
    session = TransactionalSession()
    yield session
    clean_database(session)


@pytest.fixture
def seed_site_conditions(request):
    record_count = request.param
    test_dt = datetime(
        year=2024, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc
    )
    site_conditions = []

    for i in range(record_count):
        minutes_offset = 15 * i

        site_condition = SiteConditionORM(
            site_id="TEST_ID",
            site_name="TEST_NAME",
            timestamp=test_dt + timedelta(minutes=minutes_offset),
            value=100 + i,
            unit="ft3/s",
        )
        site_conditions.append(site_condition)

    session = TransactionalSession()
    session.add_all(site_conditions)
    session.commit()
