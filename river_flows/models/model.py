import torch.nn as nn


class FlowCNN(nn.Module):
    """
    1D CNN for hourly river flow forecasting.

    Input:
        x shape = (batch, in_channels, seq_len)

    Output:
        (batch, horizon)
    """
    def __init__(
        self,
        in_channels: int,
        horizon: int = 24,
        channels: tuple[int, ...] = (64, 128, 128),
        kernel_size: int = 7,
        dropout: float = 0.15,
    ):
        super().__init__()

        if kernel_size % 2 == 0:
            raise ValueError("kernel_size should be odd for symmetric padding.")

        padding = kernel_size // 2

        conv_layers = []
        prev = in_channels

        for ch in channels:
            conv_layers += [
                nn.Conv1d(prev, ch, kernel_size=kernel_size, padding=padding),
                nn.BatchNorm1d(ch),
                nn.ReLU(),
                nn.Dropout(dropout),
            ]
            prev = ch

        self.conv = nn.Sequential(*conv_layers)

        self.head = nn.Sequential(
            nn.Linear(prev, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, horizon),
        )

    def forward(self, x):
        z = self.conv(x)      # (batch, ch, seq_len)
        z = z.mean(dim=-1)    # global avg pool over time
        return self.head(z)   # (batch, horizon)
