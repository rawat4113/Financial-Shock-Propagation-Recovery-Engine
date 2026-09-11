from pathlib import Path
import time
import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
START = "2010-01-01"

def yf_download(ticker, relative_path):
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)
    df = yf.download(ticker, start=START, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df.reset_index().to_csv(out, index=False)
    print(f"{ticker}: {len(df)} rows -> {out}")

def fred(series, relative_path):
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={START}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    out.write_bytes(r.content)
    print(f"FRED {series} -> {out}")

def world_bank(indicator, relative_path):
    out = RAW / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://api.worldbank.org/v2/country/IND/indicator/{indicator}?format=json&per_page=1000"
    data = requests.get(url, timeout=60).json()[1]
    rows = [{"date": x["date"], "value": x["value"], "indicator": indicator, "country":"IND"} for x in data]
    pd.DataFrame(rows).sort_values("date").to_csv(out, index=False)

def main():
    # 50 Indian stocks
    universe = pd.read_csv(RAW/"company_data/company_master.csv")
    frames=[]
    for _, row in universe.iterrows():
        try:
            df=yf.download(row.yahoo_ticker,start=START,auto_adjust=False,progress=False)
            if isinstance(df.columns,pd.MultiIndex): df.columns=[c[0] for c in df.columns]
            df=df.reset_index()
            if not df.empty:
                df["ticker"]=row.ticker
                df["sector"]=row.sector
                frames.append(df)
            time.sleep(0.15)
        except Exception as e:
            print("FAILED", row.yahoo_ticker, e)
    if frames:
        pd.concat(frames,ignore_index=True).to_csv(RAW/"market_data/indian_stocks.csv",index=False)

    yf_download("^GSPC","market_data/sp500.csv")
    yf_download("^IXIC","market_data/nasdaq.csv")
    yf_download("INR=X","macroeconomic_data/usdinr.csv")
    yf_download("CL=F","market_data/crude_oil.csv")
    yf_download("GC=F","market_data/gold.csv")

    fred("VIXCLS","financial_stress/us_vix.csv")
    fred("DGS10","macroeconomic_data/us10y.csv")
    fred("STLFSI4","financial_stress/fred_stlfsi4.csv")

    world_bank("NY.GDP.MKTP.CD","macroeconomic_data/india_gdp.csv")
    world_bank("FP.CPI.TOTL.ZG","macroeconomic_data/india_inflation.csv")

    print("\nPublic datasets downloaded.")
    print("Download NIFTY50, sector indices, India VIX and RBI rates from the official portals using data/raw templates.")

if __name__ == "__main__":
    main()
