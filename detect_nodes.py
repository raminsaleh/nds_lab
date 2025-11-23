from __future__ import annotations
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Literal, Optional
from .indicators import ema, atr, rolling_sigma

@dataclass
class NDSParams:
    smoothing_kind: Literal["ema","gauss","savgol"] = "ema"
    smoothing_window: int = 9
    deadzone_mode: Literal["sigma","atr"] = "sigma"
    deadzone_k: float = 0.15
    sigma_window: int = 20
    atr_window: int = 14
    prom_mode: Literal["sigma","atr"] = "atr"
    k_sigma: float = 1.0
    k_atr: float = 1.0
    epsilon_floor: float = 1.0
    tau_min_bars: int = 3
    eps_min_atr14: float = 0.2
    alpha_low: float = 0.8
    alpha_high: float = 1.2
    beta_low: float = 0.8
    beta_high: float = 1.2
    epsilon_hook: float = 0.05
    w_bars: int = 2

def _smooth_close(close: pd.Series, kind: str, window: int) -> pd.Series:
    if kind == "ema":
        return ema(close, window)
    return ema(close, window)

def _numeric_derivative(series: pd.Series) -> pd.Series:
    return pd.Series(np.gradient(series.values), index=series.index)

def _apply_deadzone(deriv: pd.Series, ref: pd.Series, mode: str, k: float) -> pd.Series:
    ref_abs = ref.abs()
    thr = (k * ref_abs).fillna(method="bfill").fillna(method="ffill")
    dz = deriv.copy()
    dz[np.abs(deriv) < thr] = 0.0
    return dz

def _prominence_ok(price: float, last_price: float, sigma_local: float, atr_local: float, mode: str, k_sigma: float, k_atr: float, eps_floor: float) -> bool:
    if pd.isna(last_price):
        return True
    delta = abs(price - last_price)
    if mode == "sigma":
        gate = (k_sigma * sigma_local) if not pd.isna(sigma_local) else 0.0
    else:
        gate = (k_atr * atr_local) if not pd.isna(atr_local) else 0.0
    gate = max(gate, eps_floor or 0.0)
    return delta >= gate

def _separation_ok(idx: int, last_idx: Optional[int], price: float, last_price: Optional[float], tau_min: int, eps_min_atr14: float, atr_local: float) -> bool:
    if last_idx is None or last_price is None or pd.isna(last_price):
        return True
    dt = idx - last_idx
    dp = abs(price - last_price)
    gate = eps_min_atr14 * (atr_local if not pd.isna(atr_local) else 0.0)
    return (dt >= tau_min) and (dp >= gate)

def _zero_crossings(sig: pd.Series) -> pd.Series:
    sign = np.sign(sig.values)
    for i in range(1, len(sign)):
        if sign[i] == 0:
            sign[i] = sign[i-1]
    cross = (np.diff(sign) != 0).astype(int)
    zc = pd.Series(np.r_[0, cross], index=sig.index).astype(bool)
    return zc

def detect_nodes(df: pd.DataFrame, params: NDSParams) -> pd.DataFrame:
    """
    Core node detection pipeline:
      1) Smooth close
      2) Numeric derivative + deadzone
      3) Zero-crossing -> tentative nodes
      4) Confirm after w bars (repaint guard)
      5) Enforce prominence/separation gates
      6) Produce output columns aligned with SPEC
    Returns a DataFrame of accepted nodes.
    """
    price = df["close"].astype(float)
    sm = _smooth_close(price, params.smoothing_kind, params.smoothing_window)
    d1 = _numeric_derivative(sm)

    ref = rolling_sigma(price, params.sigma_window) if params.deadzone_mode == "sigma" else atr(df["high"], df["low"], df["close"], params.atr_window)
    d1_dz = _apply_deadzone(d1, ref, params.deadzone_mode, params.deadzone_k)

    zc = _zero_crossings(d1_dz)
    candidates = df[zc].copy()
    candidates["bar_index"] = candidates.index
    candidates["price"] = candidates["close"]

    sig_local = rolling_sigma(price, params.sigma_window)
    atr_local = atr(df["high"], df["low"], df["close"], params.atr_window)

    accepted = []
    last_idx = None
    last_price = float("nan")

    for idx in candidates.index:
        confirm_idx = idx + params.w_bars
        if confirm_idx >= len(df):
            continue
        p_now = float(df.loc[idx, "close"])
        if not _prominence_ok(p_now, last_price, float(sig_local.loc[idx]), float(atr_local.loc[idx]), params.prom_mode, params.k_sigma, params.k_atr, params.epsilon_floor):
            continue
        if not _separation_ok(int(idx), last_idx if last_idx is not None else None, p_now, last_price if not (last_price != last_price) else None, params.tau_min_bars, params.eps_min_atr14, float(atr_local.loc[idx])):
            continue
        accepted.append(idx)
        last_idx = int(idx)
        last_price = p_now

    out = df.loc[accepted, ["time","close"]].copy()
    out.rename(columns={"close":"price"}, inplace=True)
    out["bar_index"] = out.index

    d2 = pd.Series(np.gradient(d1.values), index=d1.index)
    out["node_type"] = np.where(d2.loc[accepted] < 0, "N", "S")
    out["higher_than_prev"] = (out["price"] > out["price"].shift(1)).fillna(False)
    out["hook_quality"] = "H0"
    out["seq_label"] = None
    out["σ_t"] = sig_local.loc[accepted].values
    out["R̂"] = np.nan
    out["SL"] = np.nan
    out["TP"] = np.nan
    out["quality_score"] = 0.0

    cols = ["bar_index","time","price","node_type","higher_than_prev","hook_quality","seq_label","σ_t","R̂","SL","TP","quality_score"]
    return out[cols]
