import pandas as pd


def rolling_zscore(s, window=60):
    mean = s.rolling(window).mean()
    std = s.rolling(window).std()

    return (s - mean) / std.replace(0, pd.NA)