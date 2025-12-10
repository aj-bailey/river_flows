import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class FlowWindowDataset(Dataset):
    """
    Builds rolling windows for 1D CNN time-series forecasting.

    Returns:
        x_seq: (features, seq_len)
        y_seq: (horizon,)
        ts_target: int64 ns timestamp corresponding to the LAST step of the horizon.
    """
    def __init__(
        self,
        df,
        feature_cols,
        target_col="flow_cfs",
        seq_len=168,
        horizon=24,
        x_scaler=None,
        y_scaler=None,
        ts_col="timestamp",
    ):
        self.df = df.copy()
        self.feature_cols = feature_cols
        self.target_col = target_col
        self.seq_len = seq_len
        self.horizon = horizon
        self.x_scaler = x_scaler
        self.y_scaler = y_scaler
        self.ts_col = ts_col

        # Robust time parsing
        self.df[ts_col] = pd.to_datetime(self.df[ts_col], utc=True, errors="coerce")
        self.df = self.df.sort_values(ts_col).reset_index(drop=True)

        # Drop rows missing anything needed
        self.df = self.df.dropna(subset=feature_cols + [target_col]).reset_index(drop=True)

        X = self.df[feature_cols].values.astype(np.float32)
        y = self.df[[target_col]].values.astype(np.float32)

        if x_scaler is not None:
            X = x_scaler.transform(X).astype(np.float32)
        if y_scaler is not None:
            y = y_scaler.transform(y).astype(np.float32)

        self.X = X
        self.y = y

        # Store timestamps as int64 ns for round-trip safety
        self.timestamps = self.df[ts_col].astype("int64").to_numpy()

        # Number of valid windows
        self.max_i = len(self.df) - seq_len - horizon + 1
        self.max_i = max(self.max_i, 0)

    def __len__(self):
        return self.max_i

    def __getitem__(self, idx):
        x_seq = self.X[idx: idx + self.seq_len]  # (seq_len, features)

        y_start = idx + self.seq_len
        y_end = y_start + self.horizon
        y_seq = self.y[y_start: y_end].squeeze(-1)  # (horizon,)

        # Conv1d expects (channels, length)
        x_seq = torch.from_numpy(x_seq).transpose(0, 1)  # (features, seq_len)
        y_seq = torch.from_numpy(y_seq)

        ts_target = torch.tensor(self.timestamps[y_end - 1], dtype=torch.int64)

        return x_seq, y_seq, ts_target
