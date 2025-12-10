import json
from pathlib import Path

import joblib
import torch

from river_flows.models.model import FlowCNN


def save_artifacts(
    model,
    x_scaler,
    y_scaler,
    feature_cols,
    config,
    out_dir="artifacts",
):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    torch.save(model.state_dict(), out / "flow_cnn_state.pt")
    joblib.dump(x_scaler, out / "x_scaler.joblib")
    joblib.dump(y_scaler, out / "y_scaler.joblib")

    (out / "feature_cols.json").write_text(json.dumps(feature_cols, indent=2))
    (out / "config.json").write_text(json.dumps(config, indent=2))

    return out


def load_artifacts(out_dir="artifacts", device="cpu"):
    """
    Single source of truth loader for inference (and optional eval).
    """
    out = Path(out_dir)

    x_scaler = joblib.load(out / "x_scaler.joblib")
    y_scaler = joblib.load(out / "y_scaler.joblib")
    feature_cols = json.loads((out / "feature_cols.json").read_text())
    config = json.loads((out / "config.json").read_text())

    model = FlowCNN(
        in_channels=len(feature_cols),
        horizon=config["horizon"],
        channels=tuple(config["channels"]),
        kernel_size=config["kernel_size"],
        dropout=config["dropout"],
    ).to(device)

    state = torch.load(out / "flow_cnn_state.pt", map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    return model, x_scaler, y_scaler, feature_cols, config
