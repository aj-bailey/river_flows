from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from river_flows.orm.base import Base
from river_flows.orm.mixins import TimestampMixin


class Snotel(Base, TimestampMixin):
    __tablename__ = "snotel"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    station_triplets: Mapped[str] = mapped_column(String, primary_key=True)
    prec: Mapped[Optional[float]] = mapped_column(Float)
    tobs: Mapped[Optional[float]] = mapped_column(Float)
    wteq: Mapped[Optional[float]] = mapped_column(Float)
    snwd: Mapped[Optional[float]] = mapped_column(Float)
