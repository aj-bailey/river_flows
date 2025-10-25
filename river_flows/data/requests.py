from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class PopulateSiteConditionsRequest(BaseModel):
    start_date: str
    end_date: str
    site_id: Optional[str] = None


class GetSiteConditionsRequest(BaseModel):
    start_date: str
    end_date: str
    site_id: Optional[str] = None


class PopulateSnotelRequest(BaseModel):
    year: str
    station_triplets: str


class GetSnotelRequest(BaseModel):
    start_date: str
    end_date: str
    station_triplets: str


class PopulateONIRequest(BaseModel):
    year: int | None = None


class PopulateHourlyRiverFlowFeaturesRequest(BaseModel):
    year: int
    site_id: Optional[str] = None

class GetHRFFeaturesRequest(BaseModel):
    year: str
    site_id: str

    # @model_validator(mode='before')
    # def validate_year(self):
    #     if self.year > datetime.now().year:
    #         raise ValueError("Year is out of bounds")
    #     return self
