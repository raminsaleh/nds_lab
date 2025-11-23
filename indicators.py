from __future__ import annotations
import pandas as pd
import numpy as np

def ema(series: pd.Series, window: int) -> pd.Series:
    return series.ewm(span=window, adjust=False).mean()

def atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=window, min_periods=1).mean()

def rolling_sigma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).std(ddof=0)
