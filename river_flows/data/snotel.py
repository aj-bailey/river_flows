from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Snotel(BaseModel):
    station_triplets: str
    timestamp: datetime
    prec: Optional[float] = None
    tobs: Optional[float] = None
    wteq: Optional[float] = None
    snwd: Optional[float] = None

    class Config:
        from_attributes = True