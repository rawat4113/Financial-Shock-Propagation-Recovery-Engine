import pandas as pd


def add_market_features(df, price_col="Close", group_col="ticker"):
    df = df.copy()

    if group_col in df.columns:
        g = df.groupby(group_col, group_keys=False)

        df["return_1d"] = g[price_col].pct_change()
        df["return_5d"] = g[price_col].pct_change(5)
        df["return_20d"] = g[price_col].pct_change(20)

        df["volatility_20d"] = g["return_1d"].transform(
            lambda x: x.rolling(20).std()
        )

        df["drawdown"] = g[price_col].transform(
            lambda x: x / x.cummax() - 1
        )

    else:
        df["return_1d"] = df[price_col].pct_change()
        df["return_5d"] = df[price_col].pct_change(5)
        df["return_20d"] = df[price_col].pct_change(20)

        df["volatility_20d"] = (
            df["return_1d"].rolling(20).std()
        )

        df["drawdown"] = (
            df[price_col] / df[price_col].cummax() - 1
        )

    return df