from datetime import datetime

from pydantic import BaseModel


class SiteCondition(BaseModel):
    site_id: str
    site_name: str
    timestamp: datetime
    value: int
    unit: str
