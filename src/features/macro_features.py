import pandas as pd


def forward_fill_as_of(df, date_col="date"):
    df = df.copy()

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    df = df.dropna(subset=[date_col])
    df = df.sort_values(date_col)

    return df.ffill()