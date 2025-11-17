# nds_core.py
# Hcore for NDS: node detection + export scaffold
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np
import pandas as pd


class NodeType(Enum):
    """Simple taxonomy for nodes (will be specialized per SPEC)."""
    UNDEFINED = 0
    REVERSAL = 1
    INTERMEDIATE = 2
    TARGET = 3


@dataclass
class NDSConfig:
    """
    Configuration for price curve, smoothing and node gating.
    Adjusted later per NDS_CORE_SPEC.
    """
    price_mode: str = "HL2"   # HL2, CLOSE, HLC3
    smoothing: str = "ema"    # none, ema, sg
    ema_len: int = 13
    sg_window: int = 11       # must be odd
    sg_polyorder: int = 3
    min_distance: int = 3     # bars between nodes
    k_sigma: float = 0.25     # amplitude threshold multiplier
    vol_method: str = "atr"   # atr or std
    vol_len: int = 14


@dataclass
class Node:
    """
    NDS node with sequential ID (not letters).
    """
    id: int
    idx: int
    price: float
    t: pd.Timestamp
    node_type: NodeType = NodeType.REVERSAL
    higher_than_prev: Optional[bool] = None


class NDSDetector:
    """
    Core detector: builds a price curve, derives it, and extracts candidate nodes.
    Later we will plug in strict NDS rules (hooks, symmetry, invalidation).
    """

    def __init__(self, df: pd.DataFrame, cfg: Optional[NDSConfig] = None):
        """
        df must contain columns: ['time','open','high','low','close'].
        'time' can be string or datetime-like; gets converted to pandas.Timestamp.
        """
        self.df = df.copy()
        if not np.issubdtype(self.df["time"].dtype, np.datetime64):
            self.df["time"] = pd.to_datetime(self.df["time"])
        self.df.reset_index(drop=True, inplace=True)
        self.cfg = cfg or NDSConfig()
        self.nodes: List[Node] = []

    # ---------- helpers ----------

    def _price_curve(self) -> np.ndarray:
        pm = self.cfg.price_mode.upper()
        if pm == "HL2":
            base = (self.df["high"].values + self.df["low"].values) / 2.0
        elif pm == "HLC3":
            base = (self.df["high"].values + self.df["low"].values + self.df["close"].values) / 3.0
        else:
            base = self.df["close"].values.astype(float)
        return self._smooth(base)

    def _smooth(self, x: np.ndarray) -> np.ndarray:
        sm = self.cfg.smoothing.lower()
        if sm == "none":
            return x
        if sm == "ema":
            return pd.Series(x).ewm(span=self.cfg.ema_len, adjust=False).mean().values
        if sm == "sg":
            # Savitzky–Golay if SciPy available, else fallback to EMA
            try:
                from scipy.signal import savgol_filter
                window = int(self.cfg.sg_window)
                # ensure odd and >= polyorder+2
                if window % 2 == 0:
                    window += 1
                window = max(window, self.cfg.sg_polyorder + 2 if (self.cfg.sg_polyorder + 2) % 2 == 1 else self.cfg.sg_polyorder + 3)
                poly = min(self.cfg.sg_polyorder, window - 1)
                return savgol_filter(x, window_length=window, polyorder=poly, mode="interp")
            except Exception:
                return pd.Series(x).ewm(span=self.cfg.ema_len, adjust=False).mean().values
        # default fallback
        return x

    def _derivative(self, x: np.ndarray) -> np.ndarray:
        return np.gradient(x)

    def _atr(self, length: int) -> np.ndarray:
        h = self.df["high"].values
        l = self.df["low"].values
        c = self.df["close"].values
        prev_c = np.r_[c[0], c[:-1]]
        tr = np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))
        atr = pd.Series(tr).ewm(alpha=1 / length, adjust=False).mean().values
        return atr

    def _local_sigma(self) -> np.ndarray:
        if self.cfg.vol_method.lower() == "std":
            return (
                pd.Series(self.df["close"].values)
                .rolling(self.cfg.vol_len)
                .std()
                .fillna(method="bfill")
                .values
            )
        return self._atr(self.cfg.vol_len)

    # ---------- detection ----------

    def detect_raw_nodes(self) -> List[Node]:
        """
        Initial candidate-node detection (derivative sign-change + amplitude + min distance).
        This is a working scaffold; strict NDS conditions will refine/replace parts.
        """
        p = self._price_curve()
        d1 = self._derivative(p)
        sig = self._local_sigma()

        min_distance = max(1, int(self.cfg.min_distance))
        nodes: List[Node] = []
        node_id = 1
        last_idx = -min_distance

        sign = np.sign(d1)
        # (optional) treat tiny derivatives as zero to avoid micro flips
        eps = 1e-12

        for i in range(1, len(p) - 1):
            s_prev = sign[i - 1] if abs(d1[i - 1]) > eps else 0.0
            s_next = sign[i + 1] if abs(d1[i + 1]) > eps else 0.0

            is_peak = (s_prev > 0) and (s_next < 0)
            is_trough = (s_prev < 0) and (s_next > 0)
            if not (is_peak or is_trough):
                continue

            # spacing constraint
            if i - last_idx < min_distance:
                continue

            # amplitude constraint vs previous node
            if nodes:
                amp = abs(p[i] - nodes[-1].price)
                th = float(self.cfg.k_sigma) * float(sig[i])
                if amp < th:
                    continue

            node = Node(
                id=node_id,
                idx=i,
                price=float(p[i]),
                t=self.df.loc[i, "time"],
                node_type=NodeType.REVERSAL,
            )
            if nodes:
                node.higher_than_prev = node.price > nodes[-1].price

            nodes.append(node)
            last_idx = i
            node_id += 1

        self.nodes = nodes
        return nodes

    # ---------- sequencing (placeholder to be implemented per SPEC) ----------

    def classify_nodes_sequence(self) -> None:
        """
        Map nodes into roles (e.g., N1,S1,...) per NDS rules:
        - ascending:  N1 → S1 → N2 → S2 → N3 → S3
        - descending: S1 → N1 → S2 → N2 → S3 → N3
        Will be implemented after SPEC v0.2 is finalized.
        """
        pass

    # ---------- export ----------

    def export_for_mt5(self, path: str) -> None:
        """
        Export nodes into a CSV for MT5 indicator/EA consumption.
        Columns: node_id, bar_index, time, price, node_type, higher_than_prev
        """
        if not self.nodes:
            raise ValueError("No nodes detected. Run detect_raw_nodes() first.")
        out = pd.DataFrame(
            [
                {
                    "node_id": n.id,
                    "bar_index": n.idx,
                    "time": n.t,
                    "price": n.price,
                    "node_type": n.node_type.name,
                    "higher_than_prev": n.higher_than_prev,
                }
                for n in self.nodes
            ]
        )
        out.to_csv(path, index=False)
