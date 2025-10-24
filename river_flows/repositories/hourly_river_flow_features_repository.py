from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from river_flows.data.hourly_rf_feature import BatchHourlyRFFeatures
from river_flows.orm.hourly_rf_feature import HourlyRFFeature as HourlyRFFeatureORM
from river_flows.repositories.base import AbstractRepository


class HourlyRiverFlowFeaturesRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def upsert_records(self, records: BatchHourlyRFFeatures) -> int:
        total = 0

        for batch in records.batch_hourly_rf_features:
            hourly_rf_feature_data = [record.model_dump(exclude_unset=True) for record in batch]
            if not hourly_rf_feature_data:
                continue

            insert_stmt = insert(HourlyRFFeatureORM).values(hourly_rf_feature_data)

            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[
                    HourlyRFFeatureORM.site_id,
                    HourlyRFFeatureORM.timestamp,
                ],
                set_={
                    "date": insert_stmt.excluded.date,
                    "year": insert_stmt.excluded.year,
                    "month": insert_stmt.excluded.month,
                    "hour": insert_stmt.excluded.hour,
                    "flow_cfs": insert_stmt.excluded.flow_cfs,
                    "prec": insert_stmt.excluded.prec,
                    "tobs": insert_stmt.excluded.tobs,
                    "wteq": insert_stmt.excluded.wteq,
                    "snwd": insert_stmt.excluded.snwd,
                    "oni_value": insert_stmt.excluded.oni_value,
                    "month_sin": insert_stmt.excluded.month_sin,
                    "month_cos": insert_stmt.excluded.month_cos,
                    "hour_sin": insert_stmt.excluded.hour_sin,
                    "hour_cos": insert_stmt.excluded.hour_cos,
                    "flow_cfs_lag1": insert_stmt.excluded.flow_cfs_lag1,
                    "flow_cfs_lag3": insert_stmt.excluded.flow_cfs_lag3,
                    "flow_cfs_lag6": insert_stmt.excluded.flow_cfs_lag6,
                    "flow_cfs_lag24": insert_stmt.excluded.flow_cfs_lag24,
                    "flow_cfs_lag168": insert_stmt.excluded.flow_cfs_lag168,
                    "prec_lag1": insert_stmt.excluded.prec_lag1,
                    "prec_lag3": insert_stmt.excluded.prec_lag3,
                    "prec_lag6": insert_stmt.excluded.prec_lag6,
                    "prec_lag24": insert_stmt.excluded.prec_lag24,
                    "prec_lag168": insert_stmt.excluded.prec_lag168,
                    "tobs_lag1": insert_stmt.excluded.tobs_lag1,
                    "tobs_lag3": insert_stmt.excluded.tobs_lag3,
                    "tobs_lag6": insert_stmt.excluded.tobs_lag6,
                    "tobs_lag24": insert_stmt.excluded.tobs_lag24,
                    "tobs_lag168": insert_stmt.excluded.tobs_lag168,
                    "wteq_lag1": insert_stmt.excluded.wteq_lag1,
                    "wteq_lag3": insert_stmt.excluded.wteq_lag3,
                    "wteq_lag6": insert_stmt.excluded.wteq_lag6,
                    "wteq_lag24": insert_stmt.excluded.wteq_lag24,
                    "wteq_lag168": insert_stmt.excluded.wteq_lag168,
                    "snwd_lag1": insert_stmt.excluded.snwd_lag1,
                    "snwd_lag3": insert_stmt.excluded.snwd_lag3,
                    "snwd_lag6": insert_stmt.excluded.snwd_lag6,
                    "snwd_lag24": insert_stmt.excluded.snwd_lag24,
                    "snwd_lag168": insert_stmt.excluded.snwd_lag168,
                    # rolling stats
                    "flow_cfs_rollmean_3h": insert_stmt.excluded.flow_cfs_rollmean_3h,
                    "flow_cfs_rollstd_3h": insert_stmt.excluded.flow_cfs_rollstd_3h,
                    "flow_cfs_rollsum_3h": insert_stmt.excluded.flow_cfs_rollsum_3h,
                    "flow_cfs_rollmean_6h": insert_stmt.excluded.flow_cfs_rollmean_6h,
                    "flow_cfs_rollstd_6h": insert_stmt.excluded.flow_cfs_rollstd_6h,
                    "flow_cfs_rollsum_6h": insert_stmt.excluded.flow_cfs_rollsum_6h,
                    "flow_cfs_rollmean_24h": insert_stmt.excluded.flow_cfs_rollmean_24h,
                    "flow_cfs_rollstd_24h": insert_stmt.excluded.flow_cfs_rollstd_24h,
                    "flow_cfs_rollsum_24h": insert_stmt.excluded.flow_cfs_rollsum_24h,
                    "flow_cfs_rollmean_168h": insert_stmt.excluded.flow_cfs_rollmean_168h,
                    "flow_cfs_rollstd_168h": insert_stmt.excluded.flow_cfs_rollstd_168h,
                    "flow_cfs_rollsum_168h": insert_stmt.excluded.flow_cfs_rollsum_168h,
                    "prec_rollmean_3h": insert_stmt.excluded.prec_rollmean_3h,
                    "prec_rollstd_3h": insert_stmt.excluded.prec_rollstd_3h,
                    "prec_rollsum_3h": insert_stmt.excluded.prec_rollsum_3h,
                    "prec_rollmean_6h": insert_stmt.excluded.prec_rollmean_6h,
                    "prec_rollstd_6h": insert_stmt.excluded.prec_rollstd_6h,
                    "prec_rollsum_6h": insert_stmt.excluded.prec_rollsum_6h,
                    "prec_rollmean_24h": insert_stmt.excluded.prec_rollmean_24h,
                    "prec_rollstd_24h": insert_stmt.excluded.prec_rollstd_24h,
                    "prec_rollsum_24h": insert_stmt.excluded.prec_rollsum_24h,
                    "prec_rollmean_168h": insert_stmt.excluded.prec_rollmean_168h,
                    "prec_rollstd_168h": insert_stmt.excluded.prec_rollstd_168h,
                    "prec_rollsum_168h": insert_stmt.excluded.prec_rollsum_168h,
                    "tobs_rollmean_3h": insert_stmt.excluded.tobs_rollmean_3h,
                    "tobs_rollstd_3h": insert_stmt.excluded.tobs_rollstd_3h,
                    "tobs_rollmean_6h": insert_stmt.excluded.tobs_rollmean_6h,
                    "tobs_rollstd_6h": insert_stmt.excluded.tobs_rollstd_6h,
                    "tobs_rollmean_24h": insert_stmt.excluded.tobs_rollmean_24h,
                    "tobs_rollstd_24h": insert_stmt.excluded.tobs_rollstd_24h,
                    "tobs_rollmean_168h": insert_stmt.excluded.tobs_rollmean_168h,
                    "tobs_rollstd_168h": insert_stmt.excluded.tobs_rollstd_168h,
                    "wteq_rollmean_3h": insert_stmt.excluded.wteq_rollmean_3h,
                    "wteq_rollstd_3h": insert_stmt.excluded.wteq_rollstd_3h,
                    "wteq_rollmean_6h": insert_stmt.excluded.wteq_rollmean_6h,
                    "wteq_rollstd_6h": insert_stmt.excluded.wteq_rollstd_6h,
                    "wteq_rollmean_24h": insert_stmt.excluded.wteq_rollmean_24h,
                    "wteq_rollstd_24h": insert_stmt.excluded.wteq_rollstd_24h,
                    "wteq_rollmean_168h": insert_stmt.excluded.wteq_rollmean_168h,
                    "wteq_rollstd_168h": insert_stmt.excluded.wteq_rollstd_168h,
                    "snwd_rollmean_3h": insert_stmt.excluded.snwd_rollmean_3h,
                    "snwd_rollstd_3h": insert_stmt.excluded.snwd_rollstd_3h,
                    "snwd_rollmean_6h": insert_stmt.excluded.snwd_rollmean_6h,
                    "snwd_rollstd_6h": insert_stmt.excluded.snwd_rollstd_6h,
                    "snwd_rollmean_24h": insert_stmt.excluded.snwd_rollmean_24h,
                    "snwd_rollstd_24h": insert_stmt.excluded.snwd_rollstd_24h,
                    "snwd_rollmean_168h": insert_stmt.excluded.snwd_rollmean_168h,
                    "snwd_rollstd_168h": insert_stmt.excluded.snwd_rollstd_168h,
                    "snowmelt_proxy": insert_stmt.excluded.snowmelt_proxy,
                    "prec_tobs": insert_stmt.excluded.prec_tobs,
                    "tobs_snwd": insert_stmt.excluded.tobs_snwd,
                    "prec_efficiency": insert_stmt.excluded.prec_efficiency,
                    "oni_lag1m": insert_stmt.excluded.oni_lag1m,
                    "oni_interaction": insert_stmt.excluded.oni_interaction,
                    "updated_at": insert_stmt.excluded.updated_at,
                },
            )

            with self.session.begin():
                self.session.execute(upsert_stmt)

            total += len(hourly_rf_feature_data)

        return total

    def get_records(self) -> list:
        pass
