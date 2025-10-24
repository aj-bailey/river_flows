from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np

from river_flows.config.config import ONI_MAPPING, SITE_MAPPING, USGS_EWRSD_SITE
from river_flows.data.hourly_rf_feature import HourlyRFFeature, BatchHourlyRFFeatures
from river_flows.data.requests import PopulateHourlyRiverFlowFeaturesRequest
from river_flows.repositories.hourly_river_flow_features_repository import (
    HourlyRiverFlowFeaturesRepository,
)
from river_flows.repositories.oni_repository import ONIRepository
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.repositories.snotel_repository import SnotelRepository


class PopulateHourlyRiverFlowFeaturesHandler:
    def __init__(
        self,
        oni_repository: ONIRepository,
        site_condition_repository: SiteConditionRepository,
        snotel_repository: SnotelRepository,
        hourly_river_flow_features_repository: HourlyRiverFlowFeaturesRepository,
    ):
        self.oni_repository = oni_repository
        self.site_condition_repository = site_condition_repository
        self.snotel_repository = snotel_repository
        self.hourly_rf_feat_repository = hourly_river_flow_features_repository

    def handle(self, request_params: PopulateHourlyRiverFlowFeaturesRequest) -> int:
        # Arrange
        year = request_params.year
        site_id = request_params.site_id

        if request_params.site_id is None:
            site_id = USGS_EWRSD_SITE

        # Retrieve Data
        raw_df = self._retrieve_raw_data(year=year, site_id=site_id)

        # Clean Data
        cleaned_df = self._clean_raw_data(df=raw_df)

        # Create Features
        hourly_feats_df = self._generate_features(df=cleaned_df)

        # Store Features
        upsert_count = self._write_features(df=hourly_feats_df)

        return upsert_count

    def _retrieve_raw_data(self, year: int, site_id: str) -> pd.DataFrame:
        site_condition_cols = ["timestamp", "site_id", "value"]
        snotel_cols = ["date", "prec", "tobs", "wteq", "snwd"]

        start_dt = pd.Timestamp(year=year, month=1, day=1) - relativedelta(months=1)
        end_dt = pd.Timestamp(year=year, month=12, day=31, hour=23)
        dt_index = pd.date_range(start=start_dt, end=end_dt, freq="H")
        df = pd.DataFrame({"timestamp": dt_index})
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

        # Add Temporal Fields
        df["hour"] = df["timestamp"].dt.hour
        df["month"] = df["timestamp"].dt.month
        df["year"] = df["timestamp"].dt.year
        df["date"] = df["timestamp"].dt.date

        # Merge Site Conditions
        site_condition_data = self.site_condition_repository.get_records(
            start_date=start_dt, end_date=end_dt, site_id=site_id
        )
        site_conditions_df = pd.DataFrame([sc.model_dump() for sc in site_condition_data])[site_condition_cols]
        df = pd.merge(df, site_conditions_df, on="timestamp", how="left")
        df = df.rename(columns={"value": "flow_cfs"})

        # Merge Snotel Data
        station_triplets = SITE_MAPPING[site_id]["SNOTEL"]
        snotel_data = self.snotel_repository.get_records(
            start_date=start_dt, end_date=end_dt, station_triplets=station_triplets
        )
        snotel_df = pd.DataFrame([snotel.model_dump() for snotel in snotel_data])
        snotel_df["date"] = snotel_df["timestamp"].dt.date
        snotel_df = snotel_df[snotel_cols]
        df = pd.merge(df, snotel_df, on="date", how="left")

        # Merge ONI Data
        df["oni_triplet"] = df["month"].map(ONI_MAPPING)
        oni_data = self.oni_repository.get_records()
        oni_df = pd.DataFrame([oni.model_dump() for oni in oni_data])
        oni_long_df = oni_df.melt(id_vars="year", var_name="oni_triplet", value_name="oni_value")
        df = pd.merge(df, oni_long_df, on=["year", "oni_triplet"], how="left")
        df = df.drop(columns=["oni_triplet"])

        return df

    def _clean_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df["site_id"] = df.site_id.mode()[0]
        df["flow_cfs"].ffill(inplace=True)

        return df

    def _generate_features(self, df: pd.DataFrame) -> BatchHourlyRFFeatures:
        # cyclical time feats
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

        # lag feats
        lag_hours = [1, 3, 6, 24, 168]  # 1h, 3h, 6h, 1d, 7d
        for col in ["flow_cfs", "prec", "tobs", "wteq", "snwd"]:
            for lag in lag_hours:
                df[f"{col}_lag{lag}"] = df.groupby("site_id")[col].shift(lag)

        windows = [3, 6, 24, 168]  # 3h, 6h, 1d, 7d
        for col in ["flow_cfs", "prec", "tobs", "wteq", "snwd"]:
            for w in windows:
                df[f"{col}_rollmean_{w}h"] = df.groupby("site_id")[col].shift(1).rolling(window=w).mean()
                df[f"{col}_rollstd_{w}h"] = df.groupby("site_id")[col].shift(1).rolling(window=w).std()
                if col in ["prec", "flow_cfs"]:
                    df[f"{col}_rollsum_{w}h"] = df.groupby("site_id")[col].shift(1).rolling(window=w).sum()

        # Hydrological feats
        df["snowmelt_proxy"] = df.groupby("site_id")["wteq"].diff(periods=24) * -1
        df["prec_tobs"] = df["prec"] * df["tobs"]
        df["tobs_snwd"] = df["tobs"] * df["snwd"]
        df["prec_efficiency"] = df["prec"] / (df["snwd"] + 1)

        # Climate feats
        df["oni_lag1m"] = df.groupby("site_id")["oni_value"].shift(24 * 30)  # 1 month lag
        df["oni_interaction"] = df["oni_value"] * df["month_sin"]

        # Backfill columns, lag feats produce nulls
        df.dropna(inplace=True)

        df = df.reset_index()

        return df

    def _write_features(self, df: pd.DataFrame) -> int:
        records = df.to_dict(orient="records")

        hourly_feats = [HourlyRFFeature.model_validate(record) for record in records]
        batch_hourly_feats = BatchHourlyRFFeatures(hourly_rf_feature_data=hourly_feats)

        upsert_count = self.hourly_rf_feat_repository.upsert_records(records=batch_hourly_feats)

        return upsert_count
