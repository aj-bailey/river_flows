import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader

from river_flows.models.dataset import FlowWindowDataset
from river_flows.models.model import FlowCNN
from river_flows.models.metrics import mae_np, rmse_np, nse_np, seasonal_metrics
from river_flows.models.artifacts import save_artifacts
from river_flows.models.features import make_feature_cols


def time_split(df, ts_col="timestamp",
               train_end="2019-12-31",
               val_end="2022-12-31"):
    df = df.copy()
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    df = df.sort_values(ts_col).reset_index(drop=True)

    train = df[df[ts_col] <= pd.Timestamp(train_end, tz="UTC")]
    val = df[(df[ts_col] > pd.Timestamp(train_end, tz="UTC")) &
             (df[ts_col] <= pd.Timestamp(val_end, tz="UTC"))]
    test = df[df[ts_col] > pd.Timestamp(val_end, tz="UTC")]
    return train, val, test


def fit_scalers(train_df, feature_cols, target_col):
    x_scaler = StandardScaler()
    y_scaler = StandardScaler()
    x_scaler.fit(train_df[feature_cols].values.astype(np.float32))
    y_scaler.fit(train_df[[target_col]].values.astype(np.float32))
    return x_scaler, y_scaler


def train_one_epoch(model, loader, optimizer, device):
    model.train()
    total = 0.0
    n = 0

    for x, y, _ts in loader:
        x = x.to(device)
        y = y.to(device)

        pred = model(x)
        loss = F.mse_loss(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        bs = x.size(0)
        total += loss.item() * bs
        n += bs

    return total / max(n, 1)


@torch.no_grad()
def evaluate_metrics(model, loader, device, y_scaler=None):
    model.eval()

    total_se = 0.0
    n_elem = 0

    all_y = []
    all_p = []

    for x, y, _ts in loader:
        x = x.to(device)
        y = y.to(device)

        p = model(x)

        se = F.mse_loss(p, y, reduction="sum").item()
        total_se += se
        n_elem += y.numel()

        all_y.append(y.detach().cpu().numpy())
        all_p.append(p.detach().cpu().numpy())

    y_np = np.concatenate(all_y, axis=0)
    p_np = np.concatenate(all_p, axis=0)

    if y_scaler is not None:
        y_np = y_scaler.inverse_transform(y_np.reshape(-1, 1)).reshape(y_np.shape)
        p_np = y_scaler.inverse_transform(p_np.reshape(-1, 1)).reshape(p_np.shape)

    yt = y_np.reshape(-1)
    yp = p_np.reshape(-1)

    mse = total_se / max(n_elem, 1)

    return {
        "MSE": float(mse),
        "MAE": mae_np(yt, yp),
        "RMSE": rmse_np(yt, yp),
        "NSE": nse_np(yt, yp),
    }


@torch.no_grad()
def collect_predictions(model, loader, device, y_scaler=None):
    model.eval()

    preds, trues, times = [], [], []

    for x, y, ts in loader:
        x = x.to(device)

        pred = model(x).cpu().numpy()
        y = y.numpy()
        ts = ts.numpy()  # int64 ns

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


def run_training(
    df,
    out_dir="artifacts",
    target_col="flow_cfs",
    ts_col="timestamp",
    seq_len=168,
    horizon=24,
    channels=(64, 128, 128),
    kernel_size=7,
    dropout=0.15,
    epochs=30,
):
    feature_cols = make_feature_cols()

    df = df.copy()
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    df = df.sort_values(ts_col).reset_index(drop=True)
    df = df.dropna(subset=feature_cols + [target_col]).reset_index(drop=True)

    train_df, val_df, test_df = time_split(df, ts_col=ts_col)

    x_scaler, y_scaler = fit_scalers(train_df, feature_cols, target_col)

    train_ds = FlowWindowDataset(train_df, feature_cols, target_col,
                                 seq_len=seq_len, horizon=horizon,
                                 x_scaler=x_scaler, y_scaler=y_scaler, ts_col=ts_col)
    val_ds = FlowWindowDataset(val_df, feature_cols, target_col,
                               seq_len=seq_len, horizon=horizon,
                               x_scaler=x_scaler, y_scaler=y_scaler, ts_col=ts_col)
    test_ds = FlowWindowDataset(test_df, feature_cols, target_col,
                                seq_len=seq_len, horizon=horizon,
                                x_scaler=x_scaler, y_scaler=y_scaler, ts_col=ts_col)

    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=128, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=128, shuffle=False)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    model = FlowCNN(
        in_channels=len(feature_cols),
        horizon=horizon,
        channels=channels,
        kernel_size=kernel_size,
        dropout=dropout
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)

    best_val = float("inf")
    best_state = None

    history = {
        "epoch": [],
        "train_MSE": [],
        "val_MSE": [],
        "val_MAE": [],
        "val_RMSE": [],
        "val_NSE": [],
    }

    for epoch in range(1, epochs + 1):
        tr_loss = train_one_epoch(model, train_loader, optimizer, device)
        val_metrics = evaluate_metrics(model, val_loader, device, y_scaler)

        va_loss = val_metrics["MSE"]
        if va_loss < best_val:
            best_val = va_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        history["epoch"].append(epoch)
        history["train_MSE"].append(tr_loss)
        history["val_MSE"].append(val_metrics["MSE"])
        history["val_MAE"].append(val_metrics["MAE"])
        history["val_RMSE"].append(val_metrics["RMSE"])
        history["val_NSE"].append(val_metrics["NSE"])

        print(
            f"epoch {epoch:02d} | "
            f"train_MSE {tr_loss:.4f} | "
            f"val_MSE {val_metrics['MSE']:.4f} | "
            f"val_MAE {val_metrics['MAE']:.3f} | "
            f"val_RMSE {val_metrics['RMSE']:.3f} | "
            f"val_NSE {val_metrics['NSE']:.3f}"
        )

    if best_state is not None:
        model.load_state_dict(best_state)

    y_true, y_pred, times = collect_predictions(model, test_loader, device, y_scaler)

    yt = y_true.reshape(-1)
    yp = y_pred.reshape(-1)

    print("\nTEST overall (all horizon steps pooled):")
    print("MAE :", mae_np(yt, yp))
    print("RMSE:", rmse_np(yt, yp))
    print("NSE :", nse_np(yt, yp))

    y_true_last = y_true[:, -1]
    y_pred_last = y_pred[:, -1]

    s = seasonal_metrics(y_true_last, y_pred_last, times)
    print("\nSeasonal (based on horizon last step):")
    for k, v in s.items():
        print(k, v)

    config = {
        "seq_len": seq_len,
        "horizon": horizon,
        "channels": channels,
        "kernel_size": kernel_size,
        "dropout": dropout,
        "target_col": target_col,
        "ts_col": ts_col,
    }

    save_artifacts(model, x_scaler, y_scaler, feature_cols, config, out_dir=out_dir)

    return model, x_scaler, y_scaler, feature_cols, config, history
