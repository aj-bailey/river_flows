import pandas as pd
from river_flows.models.train import run_training

if __name__ == "__main__":
    df = pd.read_csv("rf_data.csv")

    run_training(
        df,
        out_dir="artifacts",
        seq_len=168,
        horizon=24,
        epochs=30,
    )