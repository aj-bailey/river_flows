from pydantic import BaseModel, model_validator

from river_flows.data.exceptions import ONIDataException

DEFAULT_BATCH_SIZE = 200


class ONI(BaseModel):
    year: int
    djf: float | None = None
    jfm: float | None = None
    fma: float | None = None
    mam: float | None = None
    amj: float | None = None
    mjj: float | None = None
    jja: float | None = None
    jas: float | None = None
    aso: float | None = None
    son: float | None = None
    ond: float | None = None
    ndj: float | None = None

    class Config:
        from_attributes = True

class BatchONI(BaseModel):
    batch_size: int
    batch_oni: list[list[ONI]]
    oni_data: list[ONI]

    @model_validator(mode="before")
    def batch_values(cls, values):
        if "oni_data" not in values.keys():
            raise ONIDataException()

        if "batch_size" not in values.keys():
            values["batch_size"] = DEFAULT_BATCH_SIZE

        values["batch_oni"] = []

        for i in range(0, len(values["oni_data"]), values["batch_size"]):
            batch = values["oni_data"][i : i + values["batch_size"]]
            values["batch_oni"].append(batch)

        return values
