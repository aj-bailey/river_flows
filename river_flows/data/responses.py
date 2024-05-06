from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from river_flows.data.site_condition import SiteCondition


ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseResponse(BaseModel, Generic[ModelType]):
    result: str = "success"
    error: Optional[str] = None
    data: Optional[ModelType] = None


class SiteConditionResponse(BaseResponse[SiteCondition]):
    pass
