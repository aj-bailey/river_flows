import pytest
from fastapi.testclient import TestClient

from river_flows.app import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
