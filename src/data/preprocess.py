import pandas as pd


def standardize_dates(df, date_col="Date"):
    """
    Convert date column to pandas datetime safely.

    Handles mixed date formats such as:
        2010-01-04
        2010-01-04 00:00:00
    """
    df = df.copy()

    if date_col not in df.columns:
        raise KeyError(f"Date column '{date_col}' not found")

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
        format="mixed",
    )

    df = df.dropna(subset=[date_col])
    return df.sort_values(date_col)


def remove_duplicates(df, subset=None):
    return df.drop_duplicates(subset=subset).copy()


def numeric_columns(df, exclude=None):
    """
    Convert all columns to numeric except explicitly excluded columns.
    """
    df = df.copy()
    exclude = set(exclude or [])

    for column in df.columns:
        if column not in exclude:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df