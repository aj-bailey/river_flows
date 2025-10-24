
import pytest
import vcr



TEST_PATH = "tests/fixtures/integration/app_test/"


def test__health__success(test_client):
    # Act
    response = test_client.get("/health")
    response_json = response.json()

    # Assert
    assert response_json["result"] == "GOOD"


@vcr.use_cassette(TEST_PATH + "test__populate_site_conditions__success.yaml")
def test__populate_site_conditions__success(test_client):
    # Arrange
    json_data = {
        "site_id": "09067020",
        "start_date": "05-11-2005",
        "end_date": "05-11-2006",
    }

    # Act
    response = test_client.post("/populate_site_conditions", json=json_data)
    response_json = response.json()

    # Assert
    expected_response_json = {
        "site_conditions_populated": True,
        "count_site_conditions_upserted": 32512,
    }

    assert response_json == expected_response_json


@pytest.mark.parametrize("seed_site_conditions", [10], indirect=True)
def test__site_conditions__success(
    initialize_and_clean_db, test_client, seed_site_conditions
):
    # Arrange

    # Act
    response = test_client.get(
        url="/site_conditions",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "site_id": "TEST_ID",
        },
    )
    response_json = response.json()

    # Assert
    expected_response_json = {
        "result": "success",
        "error": None,
        "data": [
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T00:00:00Z",
                "value": 100.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T00:15:00Z",
                "value": 101.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T00:30:00Z",
                "value": 102.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T00:45:00Z",
                "value": 103.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T01:00:00Z",
                "value": 104.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T01:15:00Z",
                "value": 105.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T01:30:00Z",
                "value": 106.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T01:45:00Z",
                "value": 107.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T02:00:00Z",
                "value": 108.0,
                "unit": "ft3/s",
            },
            {
                "site_id": "TEST_ID",
                "site_name": "TEST_NAME",
                "timestamp": "2024-01-01T02:15:00Z",
                "value": 109.0,
                "unit": "ft3/s",
            },
        ],
    }

    assert response_json == expected_response_json
