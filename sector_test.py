import yfinance as yf

symbols = {
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY REALTY": "^CNXREALTY",
    "NIFTY FINANCIAL SERVICES": "^CNXFIN",
    "NIFTY PSU BANK": "^CNXPSUBANK",
}

print("=" * 80)
print("SECTOR INDEX AVAILABILITY")
print("=" * 80)

for name, symbol in symbols.items():
    print(f"\n{name} -> {symbol}")

    try:
        df = yf.download(
            symbol,
            start="2010-01-01",
            end="2026-08-23",
            auto_adjust=False,
            progress=False,
        )

        print("Rows :", len(df))
        print("First:", df.index.min())
        print("Last :", df.index.max())

    except Exception as e:
        print("ERROR:", e)
