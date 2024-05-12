import vcr


TEST_PATH = 'tests/fixtures/integration/app_test/'



def test__health__success(test_client):
    # Act
    response = test_client.get("/health")
    response_json = response.json()
    
    # Assert
    assert response_json['result'] == "GOOD"

@vcr.use_cassette(TEST_PATH + 'test__populate_site_conditions__success.yaml')
def test__populate_site_conditions__success(test_client):
    # Arrange
    json_data = {"site_id": "09067020", "start_date": "05-11-2005", "end_date": "05-11-2006"}

    # Act
    response = test_client.post("/populate_site_conditions", json=json_data)
    response_json = response.json()

    # Assert
    expected_response_json = {'site_conditions_populated': True, 'count_site_conditions_upserted': 32512}

    assert response_json == expected_response_json
