from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from river_flows.data.oni import ONI
from river_flows.data.site_condition import SiteCondition
from river_flows.data.snotel import Snotel


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseResponse(BaseModel, Generic[ModelType]):
    result: str = "success"
    error: Optional[str] = None
    data: Optional[ModelType] = None


class SiteConditionResponse(BaseResponse[SiteCondition]):
    pass


class SiteConditionsResponse(BaseResponse[list[SiteCondition]]):
    pass


class SnotelResponse(BaseResponse[list[Snotel]]):
    pass


class ONIResponse(BaseResponse[list[ONI]]):
    pass
