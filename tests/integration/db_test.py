from sqlalchemy_utils import database_exists

from river_flows.config.config import DATABASE_URL


def test__db_exists():
    assert database_exists(DATABASE_URL) is True
