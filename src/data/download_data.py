from pathlib import Path
import time

import pandas as pd
import requests
import yfinance as yf


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

START = "2010-01-01"


# ---------------------------------------------------------------------------
# Yahoo Finance downloader
# ---------------------------------------------------------------------------

def yf_download(ticker, relative_path):
    """Download a Yahoo Finance dataset and save it as CSV."""
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)

    df = yf.download(
        ticker,
        start=START,
        auto_adjust=False,
        progress=False,
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    df.reset_index().to_csv(out, index=False)

    print(f"{ticker}: {len(df)} rows -> {out}")


# ---------------------------------------------------------------------------
# FRED downloader
# ---------------------------------------------------------------------------

def fred(series, relative_path):
    """Download a FRED time series and save it as CSV."""
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)

    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series}&cosd={START}"
    )

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    out.write_bytes(response.content)

    print(f"FRED {series} -> {out}")


# ---------------------------------------------------------------------------
# World Bank downloader
# ---------------------------------------------------------------------------

def world_bank(indicator, relative_path):
    """Download an India World Bank indicator."""
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)

    url = (
        "https://api.worldbank.org/v2/country/IND/indicator/"
        f"{indicator}?format=json&per_page=1000"
    )

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    payload = response.json()

    if len(payload) < 2 or payload[1] is None:
        raise RuntimeError(
            f"No World Bank data returned for indicator {indicator}"
        )

    rows = [
        {
            "date": item["date"],
            "value": item["value"],
            "indicator": indicator,
            "country": "IND",
        }
        for item in payload[1]
    ]

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values("date")

    df.to_csv(out, index=False)

    print(
        f"World Bank {indicator}: "
        f"{len(df)} rows -> {out}"
    )


# ---------------------------------------------------------------------------
# Indian stock downloader
# ---------------------------------------------------------------------------

def download_indian_stocks():
    """
    Download the 50-company Indian stock universe.

    The project keeps stable internal tickers such as LTIM and TATAMOTORS,
    while Yahoo Finance may use different/current symbols.

    source_ticker records the actual Yahoo Finance symbol used.
    """

    universe_path = RAW / "company_data" / "company_master.csv"

    universe = pd.read_csv(universe_path)

    # Yahoo Finance symbol changes / overrides.
    #
    # IMPORTANT:
    # The project ticker remains unchanged.
    # Only the Yahoo source symbol is changed.
    yahoo_overrides = {
        "LTIM": "LTM.NS",
        "TATAMOTORS": "TMPV.NS",
    }

    frames = []
    failures = []

    print("\n" + "=" * 70)
    print("INDIAN STOCK DATA DOWNLOAD")
    print("=" * 70)

    print(
        f"Target companies: {len(universe)}"
    )

    for _, row in universe.iterrows():

        project_ticker = row["ticker"]

        yahoo_ticker = yahoo_overrides.get(
            project_ticker,
            row["yahoo_ticker"],
        )

        sector = row["sector"]

        try:

            print(
                f"\nDownloading {project_ticker} "
                f"using Yahoo symbol {yahoo_ticker}..."
            )

            df = yf.download(
                yahoo_ticker,
                start=START,
                auto_adjust=False,
                progress=False,
            )

            # Flatten yfinance MultiIndex columns.
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [
                    column[0]
                    for column in df.columns
                ]

            df = df.reset_index()

            # Empty response.
            if df.empty:

                failures.append(
                    {
                        "ticker": project_ticker,
                        "yahoo_ticker": yahoo_ticker,
                        "sector": sector,
                        "reason": "empty response",
                    }
                )

                print(
                    f"FAILED {project_ticker}: "
                    f"empty response"
                )

                continue

            # Keep project ticker stable.
            df["ticker"] = project_ticker

            # Record actual Yahoo source symbol.
            df["source_ticker"] = yahoo_ticker

            # Preserve project sector.
            df["sector"] = sector

            frames.append(df)

            print(
                f"OK {project_ticker}: "
                f"{len(df):,} rows"
            )

        except Exception as exc:

            failures.append(
                {
                    "ticker": project_ticker,
                    "yahoo_ticker": yahoo_ticker,
                    "sector": sector,
                    "reason": str(exc),
                }
            )

            print(
                f"FAILED {project_ticker} "
                f"({yahoo_ticker}): {exc}"
            )

        # Small delay to reduce request pressure.
        time.sleep(0.15)

    # -----------------------------------------------------------------------
    # Save successful downloads
    # -----------------------------------------------------------------------

    if frames:

        stocks = pd.concat(
            frames,
            ignore_index=True,
        )

        output_path = (
            RAW
            / "market_data"
            / "indian_stocks.csv"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        stocks.to_csv(
            output_path,
            index=False,
        )

        downloaded_tickers = set(
            stocks["ticker"].dropna().unique()
        )

        expected_tickers = set(
            universe["ticker"].dropna().unique()
        )

        missing_tickers = sorted(
            expected_tickers - downloaded_tickers
        )

        print("\n" + "=" * 70)
        print("INDIAN STOCK DOWNLOAD SUMMARY")
        print("=" * 70)

        print(
            f"Expected companies : {len(expected_tickers)}"
        )

        print(
            f"Downloaded companies: {len(downloaded_tickers)}"
        )

        print(
            f"Missing companies   : {len(missing_tickers)}"
        )

        print(
            f"Total rows          : {len(stocks):,}"
        )

        if missing_tickers:
            print("\nMissing tickers:")

            for ticker in missing_tickers:
                print(f"  - {ticker}")

        else:
            print(
                "\nAll 50 companies downloaded successfully."
            )

        print(
            f"\nSaved to:\n{output_path}"
        )

    else:

        print(
            "\nERROR: No Indian stock datasets "
            "were successfully downloaded."
        )

    # -----------------------------------------------------------------------
    # Save failure report
    # -----------------------------------------------------------------------

    failure_path = (
        RAW
        / "market_data"
        / "indian_stock_download_failures.csv"
    )

    if failures:

        pd.DataFrame(failures).to_csv(
            failure_path,
            index=False,
        )

        print(
            f"\nFailure report saved to:\n"
            f"{failure_path}"
        )

    else:

        # Remove an old failure report if everything now succeeds.
        if failure_path.exists():
            failure_path.unlink()

        print(
            "\nNo Indian stock download failures."
        )

    return len(failures) == 0


# ---------------------------------------------------------------------------
# Main downloader
# ---------------------------------------------------------------------------

def main():

    print("\n")
    print("=" * 70)
    print("FINANCIAL SHOCK PROPAGATION & RECOVERY ENGINE")
    print("PUBLIC DATA DOWNLOADER")
    print("=" * 70)
    print(f"Start date: {START}")
    print(f"Raw data directory: {RAW}")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # 1. Indian stocks
    # -----------------------------------------------------------------------

    download_indian_stocks()

    # -----------------------------------------------------------------------
    # 2. Global market data
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("GLOBAL MARKET DATA")
    print("=" * 70)

    yf_download(
        "^GSPC",
        "market_data/sp500.csv",
    )

    yf_download(
        "^IXIC",
        "market_data/nasdaq.csv",
    )

    yf_download(
        "INR=X",
        "macroeconomic_data/usdinr.csv",
    )

    yf_download(
        "CL=F",
        "market_data/crude_oil.csv",
    )

    yf_download(
        "GC=F",
        "market_data/gold.csv",
    )

    # -----------------------------------------------------------------------
    # 3. US financial stress / macro data
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("US FINANCIAL STRESS / MACRO DATA")
    print("=" * 70)

    fred(
        "VIXCLS",
        "financial_stress/us_vix.csv",
    )

    fred(
        "DGS10",
        "macroeconomic_data/us10y.csv",
    )

    fred(
        "STLFSI4",
        "financial_stress/fred_stlfsi4.csv",
    )

    # -----------------------------------------------------------------------
    # 4. India macroeconomic data
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("INDIA MACROECONOMIC DATA")
    print("=" * 70)

    world_bank(
        "NY.GDP.MKTP.CD",
        "macroeconomic_data/india_gdp.csv",
    )

    world_bank(
        "FP.CPI.TOTL.ZG",
        "macroeconomic_data/india_inflation.csv",
    )

    # -----------------------------------------------------------------------
    # 5. Final message
    # -----------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("AUTOMATED DATA DOWNLOAD COMPLETE")
    print("=" * 70)

    print(
        "\nThe following datasets are downloaded automatically:"
    )

    print("  ✓ 50 Indian-stock universe")
    print("  ✓ S&P 500")
    print("  ✓ NASDAQ")
    print("  ✓ USD/INR")
    print("  ✓ Crude Oil")
    print("  ✓ Gold")
    print("  ✓ US VIX")
    print("  ✓ US 10Y Treasury")
    print("  ✓ FRED Financial Stress Index")
    print("  ✓ India GDP")
    print("  ✓ India Inflation")

    print(
        "\nStill requiring official Indian sources:"
    )

    print("  ⏳ NIFTY 50")
    print("  ⏳ Sector indices")
    print("  ⏳ India VIX")
    print("  ⏳ RBI interest rates")

    print("\nNext step: validate all downloaded datasets.")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()