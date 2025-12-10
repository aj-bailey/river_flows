ALL_FEATURES = [
    'timestamp', 'date', 'year', 'month', 'hour', 'site_id', 'flow_cfs',
    'prec', 'tobs', 'wteq', 'snwd', 'oni_value', 'month_sin', 'month_cos',
    'hour_sin', 'hour_cos', 'flow_cfs_lag1', 'flow_cfs_lag3',
    'flow_cfs_lag6', 'flow_cfs_lag24', 'flow_cfs_lag168', 'prec_lag1',
    'prec_lag3', 'prec_lag6', 'prec_lag24', 'prec_lag168', 'tobs_lag1',
    'tobs_lag3', 'tobs_lag6', 'tobs_lag24', 'tobs_lag168', 'wteq_lag1',
    'wteq_lag3', 'wteq_lag6', 'wteq_lag24', 'wteq_lag168', 'snwd_lag1',
    'snwd_lag3', 'snwd_lag6', 'snwd_lag24', 'snwd_lag168',
    'flow_cfs_rollmean_3h', 'flow_cfs_rollstd_3h', 'flow_cfs_rollsum_3h',
    'flow_cfs_rollmean_6h', 'flow_cfs_rollstd_6h', 'flow_cfs_rollsum_6h',
    'flow_cfs_rollmean_24h', 'flow_cfs_rollstd_24h', 'flow_cfs_rollsum_24h',
    'flow_cfs_rollmean_168h', 'flow_cfs_rollstd_168h',
    'flow_cfs_rollsum_168h', 'prec_rollmean_3h', 'prec_rollstd_3h',
    'prec_rollsum_3h', 'prec_rollmean_6h', 'prec_rollstd_6h',
    'prec_rollsum_6h', 'prec_rollmean_24h', 'prec_rollstd_24h',
    'prec_rollsum_24h', 'prec_rollmean_168h', 'prec_rollstd_168h',
    'prec_rollsum_168h', 'tobs_rollmean_3h', 'tobs_rollstd_3h',
    'tobs_rollmean_6h', 'tobs_rollstd_6h', 'tobs_rollmean_24h',
    'tobs_rollstd_24h', 'tobs_rollmean_168h', 'tobs_rollstd_168h',
    'wteq_rollmean_3h', 'wteq_rollstd_3h', 'wteq_rollmean_6h',
    'wteq_rollstd_6h', 'wteq_rollmean_24h', 'wteq_rollstd_24h',
    'wteq_rollmean_168h', 'wteq_rollstd_168h', 'snwd_rollmean_3h',
    'snwd_rollstd_3h', 'snwd_rollmean_6h', 'snwd_rollstd_6h',
    'snwd_rollmean_24h', 'snwd_rollstd_24h', 'snwd_rollmean_168h',
    'snwd_rollstd_168h', 'snowmelt_proxy', 'prec_tobs', 'tobs_snwd',
    'prec_efficiency', 'oni_lag1m', 'oni_interaction', 'created_at',
    'updated_at'
]


def make_feature_cols():
    """
    Canonical logic for which columns are used as model inputs.
    """
    drop = {
        "timestamp",
        "date", "created_at", "updated_at",
        "site_id", "flow_cfs",
        "year", "month", "hour",
    }
    return [c for c in ALL_FEATURES if c not in drop]
