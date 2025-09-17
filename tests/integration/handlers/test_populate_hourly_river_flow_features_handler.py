import pandas as pd
import pytest

from river_flows.config.config import USGS_EWRSD_SITE
from river_flows.data.requests import PopulateHourlyRiverFlowFeaturesRequest
from river_flows.handlers.populate_hourly_river_flow_features_handler import PopulateHourlyRiverFlowFeaturesHandler
from river_flows.repositories.hourly_river_flow_features_repository import HourlyRiverFlowFeaturesRepository
from river_flows.repositories.oni_repository import ONIRepository
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.repositories.snotel_repository import SnotelRepository

@pytest.fixture
def populate_hourly_rf_feat_handler(initialize_and_clean_db):
    session = initialize_and_clean_db
    site_condition_repository = SiteConditionRepository(session=session)
    oni_repository = ONIRepository(session=session)
    snotel_repository = SnotelRepository(session=session)
    hourly_rf_feat_repository = HourlyRiverFlowFeaturesRepository(session=session)

    handler = PopulateHourlyRiverFlowFeaturesHandler(
        oni_repository=oni_repository,
        site_condition_repository=site_condition_repository,
        snotel_repository=snotel_repository,
        hourly_river_flow_features_repository=hourly_rf_feat_repository
    )
    return handler

def test__handle__success(populate_hourly_rf_feat_handler):
    # Arrange
    handler = populate_hourly_rf_feat_handler
    year = 2024
    site_id = USGS_EWRSD_SITE
    request_params = PopulateHourlyRiverFlowFeaturesRequest(year=year, site_id=site_id)
    
    
    # Act
    df = handler.handle(request_params=request_params)
    
    # Assert
    pass

def test___retrieve_raw_data__success(populate_hourly_rf_feat_handler):
    # Arrange
    handler = populate_hourly_rf_feat_handler
    year = 2024
    site_id = USGS_EWRSD_SITE
    
    # Act
    df = handler._retrieve_raw_data(year=year, site_id=site_id)
    
    # Assert
    expected_cols = ['timestamp', 'month', 'year', 'date', 'site_id', 'flow_cfs', 'prec', 'tobs', 'wteq', 'snwd', 'oni_value']

    assert isinstance(df, pd.DataFrame)
    assert df.columns.to_list() == expected_cols
