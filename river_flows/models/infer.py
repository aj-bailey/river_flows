import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from river_flows.models.dataset import FlowWindowDataset
from river_flows.models.metrics import mae_np, rmse_np, nse_np


@torch.no_grad()
def collect_predictions(model, loader, device, y_scaler=None):
    model.eval()

    preds, trues, times = [], [], []

    for x, y, ts in loader:
        x = x.to(device)

        pred = model(x).cpu().numpy()
        y = y.numpy()
        ts = ts.numpy()

        if y_scaler is not None:
            pred = y_scaler.inverse_transform(pred.reshape(-1, 1)).reshape(pred.shape)
            y = y_scaler.inverse_transform(y.reshape(-1, 1)).reshape(y.shape)

        preds.append(pred)
        trues.append(y)
        times.append(ts)

    preds = np.concatenate(preds, axis=0)
    trues = np.concatenate(trues, axis=0)
    times = np.concatenate(times, axis=0)

    times = pd.to_datetime(times, unit="ns", utc=True)

    return trues, preds, times


def predict_last_step_dataframe(
    df,
    model,
    x_scaler,
    y_scaler,
    feature_cols,
    config,
    device=None,
    batch_size=256,
):
    """
    Returns a DataFrame aligned to ts_target using the last horizon step.
    """
    if device is None:
        device = torch.device(
            "mps" if torch.backends.mps.is_available()
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )

    ds = FlowWindowDataset(
        df,
        feature_cols,
        target_col=config["target_col"],
        seq_len=config["seq_len"],
        horizon=config["horizon"],
        x_scaler=x_scaler,
        y_scaler=y_scaler,
        ts_col=config["ts_col"],
    )
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False)

    y_true, y_pred, times = collect_predictions(model, loader, device, y_scaler=y_scaler)

    last_true = y_true[:, -1]
    last_pred = y_pred[:, -1]

    out = pd.DataFrame({
        "timestamp": times,
        "actual": last_true,
        "pred": last_pred,
    }).sort_values("timestamp").reset_index(drop=True)

    metrics = {
        "MAE": mae_np(out["actual"].values, out["pred"].values),
        "RMSE": rmse_np(out["actual"].values, out["pred"].values),
        "NSE": nse_np(out["actual"].values, out["pred"].values),
    }

    return out, metrics


def predict_long_dataframe(
    df,
    model,
    x_scaler,
    y_scaler,
    feature_cols,
    config,
    device=None,
    batch_size=256,
):
    """
    Expands all horizon steps into a long format DataFrame with lead_hours.
    """
    if device is None:
        device = torch.device(
            "mps" if torch.backends.mps.is_available()
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )

    horizon = config["horizon"]

    ds = FlowWindowDataset(
        df,
        feature_cols,
        target_col=config["target_col"],
        seq_len=config["seq_len"],
        horizon=horizon,
        x_scaler=x_scaler,
        y_scaler=y_scaler,
        ts_col=config["ts_col"],
    )
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False)

    y_true, y_pred, times = collect_predictions(model, loader, device, y_scaler=y_scaler)

    # times corresponds to last horizon step. Back-calc start-of-horizon time.
    base_times = times - pd.Timedelta(hours=horizon - 1)

    frames = []
    for i in range(horizon):
        frames.append(pd.DataFrame({
            "timestamp": base_times + pd.Timedelta(hours=i),
            "actual": y_true[:, i],
            "pred": y_pred[:, i],
            "lead_hours": i + 1,
        }))

    long_df = pd.concat(frames, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    return long_df
