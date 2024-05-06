from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SiteCondition(BaseModel):
    id: Optional[int] = None
    site_id: str
    site_name: str
    timestamp: datetime
    value: int
    unit: str

    class Config:
        from_attributes = True
