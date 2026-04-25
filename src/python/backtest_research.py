from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

import pandas as pd


@dataclass
class TradeEvent:
    setup_time: pd.Timestamp
    direction: str
    entry_price: float
    stop_loss: float
    target: float
    exit_reason: str
    result_points: float
    result_r: Optional[float]
    setup_valid: bool
    invalid_reason: Optional[str] = None


class BacktestResearchReport:
    """
    Governed research reporting layer for deterministic backtest outputs.
    """

    def events_to_dataframe(self, events: List[TradeEvent]) -> pd.DataFrame:
        if not events:
            return pd.DataFrame(
                columns=[
                    "setup_time",
                    "direction",
                    "entry_price",
                    "stop_loss",
                    "target",
                    "exit_reason",
                    "result_points",
                    "result_r",
                    "setup_valid",
                    "invalid_reason",
                ]
            )
        return pd.DataFrame([asdict(e) for e in events])

    def build_summary(self, events: List[TradeEvent]) -> Dict[str, Any]:
        if not events:
            return {
                "trade_count": 0,
                "valid_trade_count": 0,
                "invalid_trade_count": 0,
                "wins": 0,
                "losses": 0,
                "flats": 0,
                "total_points": 0.0,
                "avg_points": 0.0,
                "total_r": 0.0,
                "avg_r": 0.0,
            }

        valid_events = [e for e in events if e.setup_valid]
        invalid_events = [e for e in events if not e.setup_valid]

        wins = [e for e in events if e.result_points > 0]
        losses = [e for e in events if e.result_points < 0]
        flats = [e for e in events if e.result_points == 0]

        total_points = sum(e.result_points for e in events)
        r_values = [e.result_r for e in events if e.result_r is not None]
        total_r = sum(r_values) if r_values else 0.0

        return {
            "trade_count": len(events),
            "valid_trade_count": len(valid_events),
            "invalid_trade_count": len(invalid_events),
            "wins": len(wins),
            "losses": len(losses),
            "flats": len(flats),
            "total_points": total_points,
            "avg_points": total_points / len(events) if events else 0.0,
            "total_r": total_r,
            "avg_r": total_r / len(r_values) if r_values else 0.0,
        }
