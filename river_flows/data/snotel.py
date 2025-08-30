from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from river_flows.data.exceptions import SnotelDataException


DEFAULT_BATCH_SIZE = 100


class Snotel(BaseModel):
    station_triplets: str
    timestamp: datetime
    prec: Optional[float] = None
    tobs: Optional[float] = None
    wteq: Optional[float] = None
    snwd: Optional[float] = None

    class Config:
        from_attributes = True


class BatchSnotel(BaseModel):
    batch_size: int
    batch_snotel: list[list[Snotel]]
    snotel_data: list[Snotel]

    @model_validator(mode="before")
    def batch_values(cls, values):
        if "snotel_data" not in values.keys():
            raise SnotelDataException()

        if "batch_size" not in values.keys():
            values["batch_size"] = DEFAULT_BATCH_SIZE

        values["batch_snotel"] = []

        for i in range(0, len(values["snotel_data"]), values["batch_size"]):
            batch = values["snotel_data"][i : i + values["batch_size"]]
            values["batch_snotel"].append(batch)

        return values
