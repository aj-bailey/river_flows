from datetime import datetime, date

from pydantic import BaseModel, model_validator

from river_flows.data.exceptions import HourlyRFFeatureException

DEFAULT_BATCH_SIZE = 1000


class HourlyRFFeature(BaseModel):
    timestamp: datetime
    hour: int
    month: int
    year: int
    date: date
    site_id: str
    flow_cfs: float | None = None
    prec: float | None = None
    tobs: float | None = None
    wteq: float | None = None
    snwd: float | None = None
    oni_value: float | None = None
    month_sin: float
    month_cos: float
    hour_sin: float
    hour_cos: float
    flow_cfs_lag1: float | None = None
    flow_cfs_lag3: float | None = None
    flow_cfs_lag6: float | None = None
    flow_cfs_lag24: float | None = None
    flow_cfs_lag168: float | None = None
    prec_lag1: float | None = None
    prec_lag3: float | None = None
    prec_lag6: float | None = None
    prec_lag24: float | None = None
    prec_lag168: float | None = None
    tobs_lag1: float | None = None
    tobs_lag3: float | None = None
    tobs_lag6: float | None = None
    tobs_lag24: float | None = None
    tobs_lag168: float | None = None
    wteq_lag1: float | None = None
    wteq_lag3: float | None = None
    wteq_lag6: float | None = None
    wteq_lag24: float | None = None
    wteq_lag168: float | None = None
    snwd_lag1: float | None = None
    snwd_lag3: float | None = None
    snwd_lag6: float | None = None
    snwd_lag24: float | None = None
    snwd_lag168: float | None = None
    flow_cfs_rollmean_3h: float | None = None
    flow_cfs_rollstd_3h: float | None = None
    flow_cfs_rollsum_3h: float | None = None
    flow_cfs_rollmean_6h: float | None = None
    flow_cfs_rollstd_6h: float | None = None
    flow_cfs_rollsum_6h: float | None = None
    flow_cfs_rollmean_24h: float | None = None
    flow_cfs_rollstd_24h: float | None = None
    flow_cfs_rollsum_24h: float | None = None
    flow_cfs_rollmean_168h: float | None = None
    flow_cfs_rollstd_168h: float | None = None
    flow_cfs_rollsum_168h: float | None = None
    prec_rollmean_3h: float | None = None
    prec_rollstd_3h: float | None = None
    prec_rollsum_3h: float | None = None
    prec_rollmean_6h: float | None = None
    prec_rollstd_6h: float | None = None
    prec_rollsum_6h: float | None = None
    prec_rollmean_24h: float | None = None
    prec_rollstd_24h: float | None = None
    prec_rollsum_24h: float | None = None
    prec_rollmean_168h: float | None = None
    prec_rollstd_168h: float | None = None
    prec_rollsum_168h: float | None = None
    tobs_rollmean_3h: float | None = None
    tobs_rollstd_3h: float | None = None
    tobs_rollmean_6h: float | None = None
    tobs_rollstd_6h: float | None = None
    tobs_rollmean_24h: float | None = None
    tobs_rollstd_24h: float | None = None
    tobs_rollmean_168h: float | None = None
    tobs_rollstd_168h: float | None = None
    wteq_rollmean_3h: float | None = None
    wteq_rollstd_3h: float | None = None
    wteq_rollmean_6h: float | None = None
    wteq_rollstd_6h: float | None = None
    wteq_rollmean_24h: float | None = None
    wteq_rollstd_24h: float | None = None
    wteq_rollmean_168h: float | None = None
    wteq_rollstd_168h: float | None = None
    snwd_rollmean_3h: float | None = None
    snwd_rollstd_3h: float | None = None
    snwd_rollmean_6h: float | None = None
    snwd_rollstd_6h: float | None = None
    snwd_rollmean_24h: float | None = None
    snwd_rollstd_24h: float | None = None
    snwd_rollmean_168h: float | None = None
    snwd_rollstd_168h: float | None = None
    snowmelt_proxy: float | None = None
    prec_tobs: float | None = None
    tobs_snwd: float | None = None
    prec_efficiency: float | None = None
    oni_lag1m: float | None = None
    oni_interaction: float | None = None

    class Config:
        from_attributes = True


class BatchHourlyRFFeatures(BaseModel):
    batch_size: int
    batch_hourly_rf_features: list[list[HourlyRFFeature]]
    hourly_rf_feature_data: list[HourlyRFFeature]

    @model_validator(mode="before")
    def batch_values(cls, values):
        if "hourly_rf_feature_data" not in values.keys():
            raise HourlyRFFeatureException()

        if "batch_size" not in values.keys():
            values["batch_size"] = DEFAULT_BATCH_SIZE

        values["batch_hourly_rf_features"] = []

        for i in range(0, len(values["hourly_rf_feature_data"]), values["batch_size"]):
            batch = values["hourly_rf_feature_data"][i : i + values["batch_size"]]
            values["batch_hourly_rf_features"].append(batch)

        return values
