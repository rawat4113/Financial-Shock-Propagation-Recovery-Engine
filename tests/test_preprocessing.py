from src.data.preprocess import standardize_dates
import pandas as pd

def test_standardize_dates():
    x=standardize_dates(pd.DataFrame({'Date':['2020-01-01','2020-01-02']}))
    assert x['Date'].notna().all()
