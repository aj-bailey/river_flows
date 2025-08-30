from datetime import datetime
from unittest.mock import patch

from river_flows.background_jobs.save_previous_date_river_flows import (
    save_previous_date_river_flows,
)


@patch(
    "river_flows.background_jobs.save_previous_date_river_flows._get_previous_date_start_end"
)
def test__save_previous_date_river_flows__success(mock_dates):
    # Arrange / Act
    start_date = datetime.strptime("2024-09-06 00:00", "%Y-%m-%d %H:%M")
    end_date = datetime.strptime("2024-09-06 23:59", "%Y-%m-%d %H:%M")
    # import ipdb; ipdb.set_trace()
    mock_dates.return_value = (start_date, end_date)
    site_conditions_count = save_previous_date_river_flows()

    # Assert
    assert site_conditions_count == 96
