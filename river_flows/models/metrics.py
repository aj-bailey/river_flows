import numpy as np
import pandas as pd


def mae_np(y_true, y_pred):
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse_np(y_true, y_pred):
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def nse_np(y_true, y_pred):
    denom = np.sum((y_true - np.mean(y_true)) ** 2)
    if denom == 0:
        return float("nan")
    return float(1 - (np.sum((y_true - y_pred) ** 2) / denom))


def seasonal_metrics(y_true_last, y_pred_last, times):
    """
    Seasonal breakdown using last horizon step aligned to ts_target.
    """
    dfm = pd.DataFrame({
        "time": times,
        "y": y_true_last,
        "p": y_pred_last,
    })
    dfm["month"] = dfm["time"].dt.month

    seasons = {
        "winter_baseflow": [11, 12, 1, 2],
        "early_melt":      [3, 4],
        "peak_runoff":     [5, 6, 7],
        "late_summer":     [8, 9],
        "shoulder_fall":   [10],
    }

    out = {}
    for name, months in seasons.items():
        sub = dfm[dfm["month"].isin(months)]
        if len(sub) < 50:
            continue

        out[name] = {
            "MAE": mae_np(sub["y"].values, sub["p"].values),
            "RMSE": rmse_np(sub["y"].values, sub["p"].values),
            "NSE": nse_np(sub["y"].values, sub["p"].values),
            "n": len(sub)
        }

    return out
