from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator, ValidationError

from river_flows.data.exceptions import SiteConditionsException


DEFAULT_BATCH_SIZE = 5000


class SiteCondition(BaseModel):
    site_id: str
    site_name: str
    timestamp: datetime
    value: float
    unit: str

    class Config:
        from_attributes = True

class BatchSiteConditions(BaseModel):
    batch_size: int
    batch_site_conditions: list[list[SiteCondition]]

    @model_validator(mode='before')
    def batch_values(cls, values):
        if "site_conditions" not in values.keys():
            raise SiteConditionsException()

        if 'batch_size' not in values.keys():
            values['batch_size'] = DEFAULT_BATCH_SIZE

        values['batch_site_conditions'] = []

        
        for i in range(0, len(values['site_conditions']), values['batch_size']):
            batch_conditions = values['site_conditions'][i:i + values['batch_size']]
            values['batch_site_conditions'].append(batch_conditions)

        return values