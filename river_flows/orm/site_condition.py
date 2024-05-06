from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from river_flows.orm.base import Base
from river_flows.orm.mixins import TimestampMixin

class SiteCondition(Base, TimestampMixin):
    __tablename__ = "site_conditions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[str] = mapped_column(String)
    site_name: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    value: Mapped[int] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(String)
