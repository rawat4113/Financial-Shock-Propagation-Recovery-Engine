from pathlib import Path

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "market_data" / "sector_indices.csv"

START = "2010-01-01"
END = "2026-08-23"

SECTORS = {
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY REALTY": "^CNXREALTY",
    "NIFTY PSU BANK": "^CNXPSUBANK",
}


def download_sector(name, symbol):
    print(f"\nDownloading {name} using {symbol}...")

    df = yf.download(
        symbol,
        start=START,
        end=END,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        print(f"FAILED {name}: empty response")
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    required = ["Date", "Open", "High", "Low", "Close", "Volume"]

    missing = [c for c in required if c not in df.columns]

    if missing:
        print(f"FAILED {name}: missing columns {missing}")
        return None

    df = df[required].copy()

    df["Sector"] = name

    df = df[
        ["Date", "Sector", "Open", "High", "Low", "Close", "Volume"]
    ]

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])

    df = df.drop_duplicates(subset=["Date", "Sector"])

    df = df.sort_values(["Sector", "Date"])

    print(
        f"OK {name}: {len(df):,} rows | "
        f"{df['Date'].min().date()} -> {df['Date'].max().date()}"
    )

    return df


def main():
    print("=" * 80)
    print("SECTOR INDEX DATA DOWNLOAD")
    print("=" * 80)

    frames = []

    for name, symbol in SECTORS.items():
        df = download_sector(name, symbol)

        if df is not None:
            frames.append(df)

    if not frames:
        raise RuntimeError("No sector data downloaded.")

    result = pd.concat(frames, ignore_index=True)

    result = result.sort_values(
        ["Date", "Sector"]
    ).reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUT, index=False)

    expected = set(SECTORS)
    actual = set(result["Sector"])

    missing = sorted(expected - actual)

    print("\n" + "=" * 80)
    print("SECTOR DOWNLOAD SUMMARY")
    print("=" * 80)

    print(f"Expected sectors : {len(expected)}")
    print(f"Downloaded       : {len(actual)}")
    print(f"Total rows       : {len(result):,}")

    if missing:
        print("\nMissing sectors:")
        for sector in missing:
            print(f"  - {sector}")
    else:
        print("\nMissing sectors: NONE")

    print(f"\nSaved to:")
    print(OUT)


if __name__ == "__main__":
    main()
