from typing import Optional

from pydantic import BaseModel


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
