def test__health__success(test_client):
    # Act
    response = test_client.get("/health")
    response_json = response.json()
    
    # Assert
    assert response_json['result'] == "GOOD"
