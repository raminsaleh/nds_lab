from __future__ import annotations

from typing import Dict, Any, List

import pandas as pd

from src.python.backtest_research import TradeEvent
from src.python.trade_setup_builder import TradeSetup


class PerformanceAnalyticsReport:
    def summary_metrics(self, events: List[TradeEvent]) -> Dict[str, Any]:
        if not events:
            return {
                "trade_count": 0,
                "win_rate": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "expectancy_points": 0.0,
                "total_points": 0.0,
                "total_r": 0.0,
            }

        results_points = [e.result_points for e in events]
        results_r = [e.result_r for e in events if e.result_r is not None]

        wins = [x for x in results_points if x > 0]
        losses = [x for x in results_points if x < 0]

        trade_count = len(results_points)
        win_rate = len(wins) / trade_count if trade_count else 0.0
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0
        expectancy_points = sum(results_points) / trade_count if trade_count else 0.0
        total_points = sum(results_points)
        total_r = sum(results_r) if results_r else 0.0

        return {
            "trade_count": trade_count,
            "win_rate": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "expectancy_points": expectancy_points,
            "total_points": total_points,
            "total_r": total_r,
        }

    def path_metrics(self, events: List[TradeEvent]) -> Dict[str, Any]:
        if not events:
            return {
                "cumulative_points": [],
                "cumulative_r": [],
                "max_drawdown_points": 0.0,
            }

        cumulative_points: List[float] = []
        cumulative_r: List[float] = []

        running_points = 0.0
        running_r = 0.0
        peak_points = 0.0
        max_drawdown_points = 0.0

        for e in events:
            running_points += e.result_points
            cumulative_points.append(running_points)

            if e.result_r is not None:
                running_r += e.result_r
            cumulative_r.append(running_r)

            peak_points = max(peak_points, running_points)
            drawdown = peak_points - running_points
            max_drawdown_points = max(max_drawdown_points, drawdown)

        return {
            "cumulative_points": cumulative_points,
            "cumulative_r": cumulative_r,
            "max_drawdown_points": max_drawdown_points,
        }

    def streak_metrics(self, events: List[TradeEvent]) -> Dict[str, Any]:
        if not events:
            return {
                "max_win_streak": 0,
                "max_loss_streak": 0,
                "current_streak_type": "none",
                "current_streak_length": 0,
            }

        max_win_streak = 0
        max_loss_streak = 0
        current_type = "none"
        current_len = 0

        for e in events:
            if e.result_points > 0:
                new_type = "win"
            elif e.result_points < 0:
                new_type = "loss"
            else:
                new_type = "flat"

            if new_type == current_type:
                current_len += 1
            else:
                current_type = new_type
                current_len = 1

            if new_type == "win":
                max_win_streak = max(max_win_streak, current_len)
            elif new_type == "loss":
                max_loss_streak = max(max_loss_streak, current_len)

        return {
            "max_win_streak": max_win_streak,
            "max_loss_streak": max_loss_streak,
            "current_streak_type": current_type,
            "current_streak_length": current_len,
        }

    def grouped_by_source_context(
        self,
        setups: List[TradeSetup],
        events: List[TradeEvent],
    ) -> pd.DataFrame:
        if not setups or not events:
            return pd.DataFrame()

        rows = []
        for s, e in zip(setups, events):
            rows.append(
                {
                    "source_context": s.source_context,
                    "result_points": e.result_points,
                    "result_r": e.result_r,
                    "exit_reason": e.exit_reason,
                }
            )

        df = pd.DataFrame(rows)
        return (
            df.groupby("source_context", dropna=False)
            .agg(
                trade_count=("result_points", "count"),
                total_points=("result_points", "sum"),
                avg_points=("result_points", "mean"),
            )
            .reset_index()
        )

    def build_full_analytics(
        self,
        setups: List[TradeSetup],
        events: List[TradeEvent],
    ) -> Dict[str, Any]:
        return {
            "summary_metrics": self.summary_metrics(events),
            "path_metrics": self.path_metrics(events),
            "streak_metrics": self.streak_metrics(events),
            "grouped_by_source_context": self.grouped_by_source_context(setups, events),
        }
