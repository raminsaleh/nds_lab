from __future__ import annotations

from typing import List

import pandas as pd

from src.python.backtest_research import TradeEvent
from src.python.trade_setup_builder import TradeSetup


class TradeEventBuilder:
    def build(
        self,
        df: pd.DataFrame,
        setups: List[TradeSetup],
    ) -> List[TradeEvent]:
        events: List[TradeEvent] = []

        if not setups:
            return events

        if not pd.api.types.is_datetime64_any_dtype(df["time"]):
            df = df.copy()
            df["time"] = pd.to_datetime(df["time"])

        for setup in setups:
            if not setup.setup_valid:
                events.append(
                    TradeEvent(
                        setup_time=setup.setup_time,
                        direction=setup.direction,
                        entry_price=setup.entry_price,
                        stop_loss=setup.stop_loss,
                        target=setup.target,
                        exit_reason="invalid_setup",
                        result_points=0.0,
                        result_r=None,
                        setup_valid=False,
                        invalid_reason=setup.invalid_reason,
                    )
                )
                continue

            future = df[df["time"] >= setup.setup_time].copy()
            if future.empty:
                continue

            exit_reason = "final_close"
            result_points = 0.0

            if setup.direction == "long":
                stop_hit = future[future["low"] <= setup.stop_loss]
                target_hit = future[future["high"] >= setup.target]

                first_stop_time = stop_hit["time"].iloc[0] if not stop_hit.empty else None
                first_target_time = target_hit["time"].iloc[0] if not target_hit.empty else None

                if first_target_time is not None and (
                    first_stop_time is None or first_target_time <= first_stop_time
                ):
                    exit_reason = "target_hit"
                    result_points = setup.target - setup.entry_price
                elif first_stop_time is not None:
                    exit_reason = "stop_hit"
                    result_points = setup.stop_loss - setup.entry_price
                else:
                    final_close = float(future["close"].iloc[-1])
                    result_points = final_close - setup.entry_price

            else:
                stop_hit = future[future["high"] >= setup.stop_loss]
                target_hit = future[future["low"] <= setup.target]

                first_stop_time = stop_hit["time"].iloc[0] if not stop_hit.empty else None
                first_target_time = target_hit["time"].iloc[0] if not target_hit.empty else None

                if first_target_time is not None and (
                    first_stop_time is None or first_target_time <= first_stop_time
                ):
                    exit_reason = "target_hit"
                    result_points = setup.entry_price - setup.target
                elif first_stop_time is not None:
                    exit_reason = "stop_hit"
                    result_points = setup.entry_price - setup.stop_loss
                else:
                    final_close = float(future["close"].iloc[-1])
                    result_points = setup.entry_price - final_close

            risk = abs(setup.entry_price - setup.stop_loss)
            result_r = (result_points / risk) if risk != 0 else None

            events.append(
                TradeEvent(
                    setup_time=setup.setup_time,
                    direction=setup.direction,
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    target=setup.target,
                    exit_reason=exit_reason,
                    result_points=result_points,
                    result_r=result_r,
                    setup_valid=setup.setup_valid,
                    invalid_reason=setup.invalid_reason,
                )
            )

        return events
