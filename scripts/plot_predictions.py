import pandas as pd
import matplotlib.pyplot as plt
import torch

from river_flows.models.artifacts import load_artifacts
from river_flows.models.infer import predict_last_step_dataframe


if __name__ == "__main__":
    df = pd.read_csv("rf_data.csv")

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    model, x_scaler, y_scaler, feature_cols, config = load_artifacts("artifacts", device=device)

    pred_df, metrics = predict_last_step_dataframe(
        df,
        model,
        x_scaler,
        y_scaler,
        feature_cols,
        config,
        device=device,
    )

    print("Aligned last-step metrics:")
    for k, v in metrics.items():
        print(k, v)

    plt.figure(figsize=(12, 4))
    plt.plot(pred_df["timestamp"], pred_df["actual"], label="Actual")
    plt.plot(pred_df["timestamp"], pred_df["pred"], label="Pred")
    plt.title(f"Actual vs Predicted Flow (last step of {config['horizon']}h horizon)")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Flow (cfs)")
    plt.legend()
    plt.tight_layout()
    plt.show()

    if len(pred_df):
        max_t = pred_df["timestamp"].max()
        recent = pred_df[pred_df["timestamp"] >= (max_t - pd.Timedelta(days=90))]

        plt.figure(figsize=(12, 4))
        plt.plot(recent["timestamp"], recent["actual"], label="Actual")
        plt.plot(recent["timestamp"], recent["pred"], label="Pred")
        plt.title("Actual vs Predicted Flow (last 90 days)")
        plt.xlabel("Time (UTC)")
        plt.ylabel("Flow (cfs)")
        plt.legend()
        plt.tight_layout()
        plt.show()
