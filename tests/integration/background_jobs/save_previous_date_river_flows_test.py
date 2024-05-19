from river_flows.background_jobs.save_previous_date_river_flows import save_previous_date_river_flows

def test__save_previous_date_river_flows__success():
    # Arrange / Act
    site_conditions_count = save_previous_date_river_flows()
    
    # Assert
    assert site_conditions_count == 96