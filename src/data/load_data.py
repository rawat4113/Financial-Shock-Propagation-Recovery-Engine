from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def load_csv(relative_path):
    return pd.read_csv(ROOT / relative_path, parse_dates=True)
