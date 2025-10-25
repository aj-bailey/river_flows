from river_flows.data.hourly_rf_feature import HourlyRFFeature
from river_flows.repositories.hourly_river_flow_features_repository import HourlyRiverFlowFeaturesRepository

class HourlyRiverFlowFeaturesHandler:
    def __init__(
            self,
            hourly_river_flow_features_repository: HourlyRiverFlowFeaturesRepository
    ):
        self.hourly_river_flow_features_repository = hourly_river_flow_features_repository
    
    def handle(self, year: int, site_id: str) -> list[HourlyRFFeature]:
        feature_data = self.hourly_river_flow_features_repository.get_records(year=year, site_id=site_id)
        
        return feature_data