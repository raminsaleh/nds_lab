# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class QAConfig:
    timeframe: str = "15T"   # M15
    tz: str = "UTC"
    outlier_z: float = 6.0

class DataQA:
    def __init__(self, df: pd.DataFrame, cfg: Optional[QAConfig] = None):
        self.df = df.copy()
        self.cfg = cfg or QAConfig()
        self.issues = []

    def _log(self, kind: str, msg: str, **extra):
        self.issues.append({"type": kind, "msg": msg, **extra})

    # 1) ساختار ستون‌ها
    def schema(self):
        required = ["time","open","high","low","close"]
        missing = [c for c in required if c not in self.df.columns]
        if missing:
            self._log("error","missing columns", missing=missing)
        return self

    # 2) زمان‌ها به UTC و صعودی + تکراری‌ها
    def time_parse(self):
        try:
            self.df["time"] = pd.to_datetime(self.df["time"], utc=True)
        except Exception as e:
            self._log("error","time parse failed", error=str(e))
            return self
        if not self.df["time"].is_monotonic_increasing:
            self._log("warn","time not strictly increasing")
            self.df.sort_values("time", inplace=True)
        dup = int(self.df["time"].duplicated().sum())
        if dup:
            self._log("error","duplicate timestamps", count=dup)
        return self

    # 3) sanity چک OHLC
    def ohlc_sanity(self):
        s = self.df
        bad = (s["low"] > s[["open","close"]].min(axis=1)) | \
              (s["high"] < s[["open","close"]].max(axis=1)) | \
              (s[["open","high","low","close"]] < 0).any(axis=1)
        n_bad = int(bad.sum())
        if n_bad:
            self._log("error","OHLC sanity failed", rows=n_bad)
        return self

    # 4) برآورد گپ‌ها (تقریبی)
    def gaps(self):
        if self.df.empty:
            self._log("warn","empty dataframe")
            return self
        rng = pd.date_range(self.df["time"].min(), self.df["time"].max(),
                            freq=self.cfg.timeframe, tz="UTC")
        missing = int(len(rng.difference(self.df["time"])))
        if missing:
            self._log("warn","approx missing bars", count=missing)
        return self

    # 5) آوتلایرهای قیمت (z-score ساده)
    def outliers(self):
        if self.df.empty:
            return self
        c = self.df["close"].astype(float)
        z = ((c - c.mean()) / (c.std() + 1e-9)).abs()
        n = int((z > self.cfg.outlier_z).sum())
        if n:
            self._log("warn","price outliers detected", count=n, z=self.cfg.outlier_z)
        return self

    def report(self) -> Dict[str, Any]:
        return {"n_rows": int(len(self.df)), "issues": self.issues}

# میان‌بر اجرای سریع روی یک CSV
def qa_csv(path: str, timeframe: str = "15T") -> Dict[str, Any]:
    df = pd.read_csv(path)
    qa = DataQA(df, QAConfig(timeframe=timeframe))
    qa.schema().time_parse().ohlc_sanity().gaps().outliers()
    return qa.report()
