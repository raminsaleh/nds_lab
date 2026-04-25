from __future__ import annotations

from typing import Dict, Any, List

from src.python.backtest_research import TradeEvent
from src.python.trade_setup_builder import TradeSetup


class ResearchAuditReport:
    def failure_buckets(self, events: List[TradeEvent]) -> Dict[str, int]:
        buckets: Dict[str, int] = {}
        for e in events:
            buckets[e.exit_reason] = buckets.get(e.exit_reason, 0) + 1
        return buckets

    def invalidation_buckets(
        self,
        setups: List[TradeSetup],
        events: List[TradeEvent],
    ) -> Dict[str, int]:
        buckets: Dict[str, int] = {}

        for s in setups:
            if s.invalid_reason:
                buckets[s.invalid_reason] = buckets.get(s.invalid_reason, 0) + 1

        for e in events:
            if e.invalid_reason:
                buckets[e.invalid_reason] = buckets.get(e.invalid_reason, 0) + 1

        return buckets

    def source_context_buckets(self, setups: List[TradeSetup]) -> Dict[str, int]:
        buckets: Dict[str, int] = {}
        for s in setups:
            buckets[s.source_context] = buckets.get(s.source_context, 0) + 1
        return buckets

    def event_outcome_buckets(self, events: List[TradeEvent]) -> Dict[str, int]:
        buckets = {"positive": 0, "negative": 0, "flat": 0}
        for e in events:
            if e.result_points > 0:
                buckets["positive"] += 1
            elif e.result_points < 0:
                buckets["negative"] += 1
            else:
                buckets["flat"] += 1
        return buckets

    def build_full_audit(
        self,
        setups: List[TradeSetup],
        events: List[TradeEvent],
    ) -> Dict[str, Any]:
        return {
            "failure_buckets": self.failure_buckets(events),
            "invalidation_buckets": self.invalidation_buckets(setups, events),
            "source_context_buckets": self.source_context_buckets(setups),
            "event_outcome_buckets": self.event_outcome_buckets(events),
        }
