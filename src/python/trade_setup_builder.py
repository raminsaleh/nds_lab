from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

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
        last_123 = self._find_last_valid_123(bundle)
        target_anchor = self._find_target_anchor(
            sequenced_nodes=sequenced_nodes,
            direction=direction_context.direction,
        )
        candidate_nodes = self._direction_compatible_nodes(
            sequenced_nodes=sequenced_nodes,
            direction=direction_context.direction,
        )

        for node in candidate_nodes:
            entry_price = float(getattr(node, "price"))
            setup_time = getattr(node, "t")

            source_parts = ["direction", "sequence"]
            invalid_reason: Optional[str] = None

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

    def _find_last_valid_123(self, bundle: PatternBundle) -> Optional[object]:
        valid = [p for p in bundle.patterns_123 if p.is_valid]
        return valid[-1] if valid else None

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

    def _find_target_anchor(
        self,
        sequenced_nodes: List[object],
        direction: str,
    ) -> Optional[Tuple[str, float]]:
        for node in reversed(sequenced_nodes):
            if not getattr(node, "sequence_valid", False):
                continue
            state = getattr(getattr(node, "sequence_state", None), "value", "")
            price = float(getattr(node, "price"))
            if direction == "long" and state in {"N1", "N2"}:
                return state, price
            if direction == "short" and state in {"S1", "S2"}:
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
