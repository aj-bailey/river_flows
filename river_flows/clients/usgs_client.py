import requests

from river_flows.config.config import USGS_EWRSD_SITE, USGS_URL
from river_flows.data.site_condition import SiteCondition

class USGSClient():
    def __init__(self, base_url: str = USGS_URL, site: str = USGS_EWRSD_SITE):
        self.usgs_url = f"{base_url}/?format=json&sites={site}"

    def current_river_flow(self) -> SiteCondition:
        response = requests.get(self.usgs_url)
        response.raise_for_status()
        response_json = response.json()

        site_condition = self._parse_response(response_json)

        return site_condition

    
    def _parse_response(self, site_data: dict) -> SiteCondition:
        site_dict = {}

        site_dict['site_id'] = site_data["value"]["timeSeries"][1]['sourceInfo']['siteCode'][0]['value']
        site_dict['site_name'] = site_data["value"]["timeSeries"][1]['sourceInfo']['siteName']
        site_dict['timestamp'] = site_data["value"]["timeSeries"][1]['values'][0]['value'][0]['dateTime']
        site_dict['value'] = site_data["value"]["timeSeries"][1]['values'][0]['value'][0]['value']
        site_dict['unit'] = site_data["value"]["timeSeries"][1]['variable']['unit']['unitCode']

        return SiteCondition(**site_dict)
