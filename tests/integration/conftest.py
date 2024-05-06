import pytest
from sqlalchemy import create_engine

from river_flows.utils.db import TransactionalSession
from tests.utils.db import clean_database


@pytest.fixture
def db_engine():
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/river_flows-test")

    return engine

@pytest.fixture
def initialize_and_clean_db():
    session = TransactionalSession()
    yield session
    clean_database(session)
