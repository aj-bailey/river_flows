from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from river_flows.orm.base import Base
from river_flows.orm.mixins import TimestampMixin

class SiteCondition(Base, TimestampMixin):
    __tablename__ = "site_conditions"
    
    site_id: Mapped[str] = mapped_column(String, primary_key=True)
    site_name: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    value: Mapped[int] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
