from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ["time", "open", "high", "low", "close"]

def read_ohlc_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")
    try:
        df["time"] = pd.to_datetime(df["time"])
    except Exception:
        pass
    return df[REQUIRED_COLUMNS].copy()
