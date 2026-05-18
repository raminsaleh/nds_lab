from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd

from src.python.pattern_bundle import PatternBundle


@dataclass
class DirectionContext:
    timestamp: pd.Timestamp
    direction_owner: str
    direction: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None


@dataclass
class TradeSetup:
    setup_time: pd.Timestamp
    direction: str
    entry_price: float
    stop_loss: float
    target: float
    source_context: str
    setup_valid: bool = True
    invalid_reason: Optional[str] = None


class TradeSetupBuilder:
    def __init__(
        self,
        stop_anchor_buffer_points: float = 2.0,
        target_anchor_buffer_points: float = 1.0,
    ) -> None:
        self.stop_anchor_buffer_points = stop_anchor_buffer_points
        self.target_anchor_buffer_points = target_anchor_buffer_points

    def build(
        self,
        sequenced_nodes: List[object],
        bundle: PatternBundle,
        direction_context: DirectionContext,
    ) -> List[TradeSetup]:
        setups: List[TradeSetup] = []

        if not direction_context.is_valid:
            return [
                TradeSetup(
                    setup_time=direction_context.timestamp,
                    direction=direction_context.direction,
                    entry_price=0.0,
                    stop_loss=0.0,
                    target=0.0,
                    source_context="invalid-direction-context",
                    setup_valid=False,
                    invalid_reason=direction_context.invalid_reason or "direction_context_invalid",
                )
            ]

        price_map = self._build_price_map(sequenced_nodes)
        candidate_nodes = self._direction_compatible_nodes(
            sequenced_nodes=sequenced_nodes,
            direction=direction_context.direction,
        )

        for node in candidate_nodes:
            entry_price = float(getattr(node, "price"))
            setup_time = pd.Timestamp(getattr(node, "t"))

            source_parts = ["direction", "sequence"]
            invalid_reason: Optional[str] = None

            last_123 = self._find_last_valid_123_before_time(
                bundle=bundle,
                sequenced_nodes=sequenced_nodes,
                cutoff_time=setup_time,
                entry_price=entry_price,
                direction=direction_context.direction,
            )
            stop_loss = self._project_stop_loss_from_123(
                price_map=price_map,
                last_123=last_123,
                direction=direction_context.direction,
            )
            if stop_loss is None:
                invalid_reason = "missing_123_anchor"
                stop_loss = 0.0
            else:
                source_parts.append("123-anchor")

            target_anchor = self._find_target_anchor_before_time(
                sequenced_nodes=sequenced_nodes,
                direction=direction_context.direction,
                cutoff_time=setup_time,
                entry_price=entry_price,
            )
            target = self._project_target_from_anchor(
                target_anchor=target_anchor,
                direction=direction_context.direction,
            )
            if target is None:
                if invalid_reason is None:
                    invalid_reason = "missing_target_anchor"
                target = entry_price
            else:
                source_parts.append("target-anchor")

            if invalid_reason is None:
                if direction_context.direction == "long":
                    if stop_loss >= entry_price:
                        invalid_reason = "stop_not_below_entry"
                    elif target <= entry_price:
                        invalid_reason = "target_not_above_entry"
                else:
                    if stop_loss <= entry_price:
                        invalid_reason = "stop_not_above_entry"
                    elif target >= entry_price:
                        invalid_reason = "target_not_below_entry"

            setups.append(
                TradeSetup(
                    setup_time=setup_time,
                    direction=direction_context.direction,
                    entry_price=entry_price,
                    stop_loss=stop_loss,
                    target=target,
                    source_context="+".join(source_parts),
                    setup_valid=(invalid_reason is None),
                    invalid_reason=invalid_reason,
                )
            )

        return setups

    def _build_price_map(self, sequenced_nodes: List[object]) -> Dict[int, float]:
        out: Dict[int, float] = {}
        for node in sequenced_nodes:
            out[int(getattr(node, "node_id"))] = float(getattr(node, "price"))
        return out

    def _direction_compatible_nodes(
        self,
        sequenced_nodes: List[object],
        direction: str,
    ) -> List[object]:
        out: List[object] = []
        for node in sequenced_nodes:
            if not getattr(node, "sequence_valid", False):
                continue
            state = getattr(getattr(node, "sequence_state", None), "value", "")
            if direction == "long" and state.startswith("N"):
                out.append(node)
            elif direction == "short" and state.startswith("S"):
                out.append(node)
        return out

    def _find_last_valid_123_before_time(
        self,
        bundle: PatternBundle,
        sequenced_nodes: List[object],
        cutoff_time: pd.Timestamp,
        entry_price: float,
        direction: str,
    ) -> Optional[object]:
        node_time_map: Dict[int, pd.Timestamp] = {
            int(getattr(node, "node_id")): pd.Timestamp(getattr(node, "t"))
            for node in sequenced_nodes
        }

        node_price_map: Dict[int, float] = {
            int(getattr(node, "node_id")): float(getattr(node, "price"))
            for node in sequenced_nodes
        }

        eligible_patterns: List[Tuple[pd.Timestamp, object]] = []

        for pattern in bundle.patterns_123:
            if not getattr(pattern, "is_valid", False):
                continue

            anchor_ids = getattr(pattern, "anchor_node_ids", [])
            if not anchor_ids:
                continue

            anchor_times = [
                node_time_map[node_id]
                for node_id in anchor_ids
                if node_id in node_time_map
            ]
            if len(anchor_times) != len(anchor_ids):
                continue

            anchor_prices = [
                node_price_map[node_id]
                for node_id in anchor_ids
                if node_id in node_price_map
            ]
            if len(anchor_prices) != len(anchor_ids):
                continue

            pattern_time = max(anchor_times)
            if pattern_time >= cutoff_time:
                continue

            if direction == "long":
                projected_stop = min(anchor_prices) - self.stop_anchor_buffer_points
                if projected_stop < entry_price:
                    eligible_patterns.append((pattern_time, pattern))
            else:
                projected_stop = max(anchor_prices) + self.stop_anchor_buffer_points
                if projected_stop > entry_price:
                    eligible_patterns.append((pattern_time, pattern))

        if not eligible_patterns:
            return None

        eligible_patterns.sort(key=lambda x: x[0])
        return eligible_patterns[-1][1]

    def _project_stop_loss_from_123(
        self,
        price_map: Dict[int, float],
        last_123: Optional[object],
        direction: str,
    ) -> Optional[float]:
        if last_123 is None:
            return None

        anchor_ids = getattr(last_123, "anchor_node_ids", [])
        anchor_prices = [price_map[node_id] for node_id in anchor_ids if node_id in price_map]
        if not anchor_prices:
            return None

        if direction == "long":
            return min(anchor_prices) - self.stop_anchor_buffer_points
        return max(anchor_prices) + self.stop_anchor_buffer_points

    def _find_target_anchor_before_time(
        self,
        sequenced_nodes: List[object],
        direction: str,
        cutoff_time: pd.Timestamp,
        entry_price: float,
    ) -> Optional[Tuple[str, float]]:
        eligible_nodes: List[object] = []

        for node in sequenced_nodes:
            node_time = pd.Timestamp(getattr(node, "t"))
            if node_time >= cutoff_time:
                continue
            if not getattr(node, "sequence_valid", False):
                continue
            eligible_nodes.append(node)

        for node in reversed(eligible_nodes):
            state = getattr(getattr(node, "sequence_state", None), "value", "")
            price = float(getattr(node, "price"))

            if direction == "long" and state in {"N1", "N2"}:
                projected_target = price + self.target_anchor_buffer_points
                if projected_target > entry_price:
                    return state, price

            if direction == "short" and state in {"S1", "S2"}:
                projected_target = price - self.target_anchor_buffer_points
                if projected_target < entry_price:
                    return state, price

        return None

    def _project_target_from_anchor(
        self,
        target_anchor: Optional[Tuple[str, float]],
        direction: str,
    ) -> Optional[float]:
        if target_anchor is None:
            return None

        _, anchor_price = target_anchor
        if direction == "long":
            return anchor_price + self.target_anchor_buffer_points
        return anchor_price - self.target_anchor_buffer_points
