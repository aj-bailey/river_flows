from datetime import datetime, date as d

from sqlalchemy import Integer, String, Float, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

from river_flows.orm.base import Base
from river_flows.orm.mixins import TimestampMixin


class HourlyRFFeature(Base, TimestampMixin):
    __tablename__ = "hourly_river_flow_features"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    date: Mapped[d] = mapped_column(Date, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    hour: Mapped[int] = mapped_column(Integer, nullable=False)
    site_id: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)

    flow_cfs: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd: Mapped[float | None] = mapped_column(Float, nullable=True)
    oni_value: Mapped[float | None] = mapped_column(Float, nullable=True)

    month_sin: Mapped[float] = mapped_column(Float, nullable=False)
    month_cos: Mapped[float] = mapped_column(Float, nullable=False)
    hour_sin: Mapped[float] = mapped_column(Float, nullable=False)
    hour_cos: Mapped[float] = mapped_column(Float, nullable=False)

    flow_cfs_lag1: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_lag3: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_lag6: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_lag24: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_lag168: Mapped[float | None] = mapped_column(Float, nullable=True)

    prec_lag1: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_lag3: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_lag6: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_lag24: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_lag168: Mapped[float | None] = mapped_column(Float, nullable=True)

    tobs_lag1: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_lag3: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_lag6: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_lag24: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_lag168: Mapped[float | None] = mapped_column(Float, nullable=True)

    wteq_lag1: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_lag3: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_lag6: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_lag24: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_lag168: Mapped[float | None] = mapped_column(Float, nullable=True)

    snwd_lag1: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_lag3: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_lag6: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_lag24: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_lag168: Mapped[float | None] = mapped_column(Float, nullable=True)

    flow_cfs_rollmean_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollstd_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollsum_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollmean_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollstd_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollsum_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollmean_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollstd_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollsum_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollmean_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollstd_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    flow_cfs_rollsum_168h: Mapped[float | None] = mapped_column(Float, nullable=True)

    prec_rollmean_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollstd_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollsum_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollmean_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollstd_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollsum_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollmean_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollstd_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollsum_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollmean_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollstd_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_rollsum_168h: Mapped[float | None] = mapped_column(Float, nullable=True)

    tobs_rollmean_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollstd_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollmean_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollstd_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollmean_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollstd_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollmean_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_rollstd_168h: Mapped[float | None] = mapped_column(Float, nullable=True)

    wteq_rollmean_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollstd_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollmean_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollstd_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollmean_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollstd_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollmean_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    wteq_rollstd_168h: Mapped[float | None] = mapped_column(Float, nullable=True)

    snwd_rollmean_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollstd_3h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollmean_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollstd_6h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollmean_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollstd_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollmean_168h: Mapped[float | None] = mapped_column(Float, nullable=True)
    snwd_rollstd_168h: Mapped[float | None] = mapped_column(Float, nullable=True)

    snowmelt_proxy: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_tobs: Mapped[float | None] = mapped_column(Float, nullable=True)
    tobs_snwd: Mapped[float | None] = mapped_column(Float, nullable=True)
    prec_efficiency: Mapped[float | None] = mapped_column(Float, nullable=True)
    oni_lag1m: Mapped[float | None] = mapped_column(Float, nullable=True)
    oni_interaction: Mapped[float | None] = mapped_column(Float, nullable=True)
