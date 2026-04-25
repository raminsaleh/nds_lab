from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import pandas as pd

from src.python.trade_setup_builder import DirectionContext


@dataclass
class MultiTimeframeContext:
    timestamp: pd.Timestamp
    higher_timeframe_label: str
    lower_timeframe_label: str
    direction_owner: str
    entry_owner: str
    higher_direction: str
    direction_basis: str
    lower_cycle_closure_state: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None


class MultiTimeframeOrchestrator:
    """
    Governed multiframe orchestration scaffold.
    """

    def build_context(
        self,
        higher_sequenced_nodes: List[object],
        lower_sequenced_nodes: List[object],
        higher_timeframe_label: str,
        lower_timeframe_label: str,
    ) -> MultiTimeframeContext:
        valid_higher = [n for n in higher_sequenced_nodes if getattr(n, "sequence_valid", False)]
        valid_lower = [n for n in lower_sequenced_nodes if getattr(n, "sequence_valid", False)]

        if not valid_higher:
            ts = pd.Timestamp.utcnow()
            if valid_lower:
                ts = getattr(valid_lower[-1], "t")
            return MultiTimeframeContext(
                timestamp=ts,
                higher_timeframe_label=higher_timeframe_label,
                lower_timeframe_label=lower_timeframe_label,
                direction_owner="higher_timeframe",
                entry_owner="lower_timeframe",
                higher_direction="unknown",
                direction_basis="missing-higher-sequence",
                lower_cycle_closure_state=self._infer_lower_cycle_closure(valid_lower),
                is_valid=False,
                invalid_reason="missing_higher_timeframe_direction",
            )

        higher_direction, direction_basis = self._infer_higher_direction(valid_higher)

        ts = getattr(valid_higher[-1], "t")
        if valid_lower:
            ts = max(ts, getattr(valid_lower[-1], "t"))

        lower_cycle_closure_state = self._infer_lower_cycle_closure(valid_lower)
        is_valid = higher_direction in {"long", "short"}
        invalid_reason = None if is_valid else "unknown_higher_direction"

        return MultiTimeframeContext(
            timestamp=ts,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
            direction_owner="higher_timeframe",
            entry_owner="lower_timeframe",
            higher_direction=higher_direction,
            direction_basis=direction_basis,
            lower_cycle_closure_state=lower_cycle_closure_state,
            is_valid=is_valid,
            invalid_reason=invalid_reason,
        )

    def to_direction_context(self, context: MultiTimeframeContext) -> DirectionContext:
        return DirectionContext(
            timestamp=context.timestamp,
            direction_owner=context.direction_owner,
            direction=context.higher_direction,
            is_valid=context.is_valid,
            invalid_reason=context.invalid_reason,
        )

    def _infer_higher_direction(self, valid_higher_nodes: List[object]) -> Tuple[str, str]:
        states = [getattr(getattr(n, "sequence_state", None), "value", "") for n in valid_higher_nodes]
        last_state = states[-1] if states else ""

        has_n1 = "N1" in states
        has_n2 = "N2" in states
        has_s1 = "S1" in states
        has_s2 = "S2" in states

        if has_n1 and has_n2 and last_state.startswith("N"):
            return "long", "open-node-pair-n"
        if has_s1 and has_s2 and last_state.startswith("S"):
            return "short", "open-node-pair-s"

        if last_state.startswith("N"):
            return "long", "sequence-fallback"
        if last_state.startswith("S"):
            return "short", "sequence-fallback"

        return "unknown", "unknown"

    def _infer_lower_cycle_closure(self, valid_lower_nodes: List[object]) -> str:
        if not valid_lower_nodes:
            return "unknown"

        state = getattr(getattr(valid_lower_nodes[-1], "sequence_state", None), "value", "")

        if state in {"N3", "S3"}:
            return "closed_first"
        if state in {"N1", "S1", "N2", "S2"}:
            return "not_terminal"
        return "unknown"
