from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class SequenceState(Enum):
    N1 = "N1"
    S1 = "S1"
    N2 = "N2"
    S2 = "S2"
    N3 = "N3"
    S3 = "S3"
    UNKNOWN = "UNKNOWN"


@dataclass
class SequencedNode:
    node_id: int
    idx: int
    price: float
    t: object
    raw_higher_than_prev: Optional[bool]
    sequence_state: SequenceState
    sequence_valid: bool
    invalid_reason: Optional[str] = None


class SequenceEngine:
    """
    First governed scaffold for ascending / descending sequence assignment.

    This layer does not invent discretionary structure.
    It assigns sequential labels to already-detected nodes and preserves
    explicit validity state.
    """

    def assign_and_validate_ascending(self, raw_nodes: List[object]) -> List[SequencedNode]:
        return self._assign(raw_nodes, ascending=True)

    def assign_and_validate_descending(self, raw_nodes: List[object]) -> List[SequencedNode]:
        return self._assign(raw_nodes, ascending=False)

    def _assign(self, raw_nodes: List[object], ascending: bool) -> List[SequencedNode]:
        out: List[SequencedNode] = []
        if not raw_nodes:
            return out

        cycle = [
            SequenceState.N1,
            SequenceState.S1,
            SequenceState.N2,
            SequenceState.S2,
            SequenceState.N3,
            SequenceState.S3,
        ]
        if not ascending:
            cycle = [
                SequenceState.S1,
                SequenceState.N1,
                SequenceState.S2,
                SequenceState.N2,
                SequenceState.S3,
                SequenceState.N3,
            ]

        prev_price: Optional[float] = None
        for i, node in enumerate(raw_nodes):
            state = cycle[i % len(cycle)]
            price = float(getattr(node, "price"))

            invalid_reason = None
            is_valid = True

            if prev_price is not None and price == prev_price:
                is_valid = False
                invalid_reason = "flat_price_relation"

            out.append(
                SequencedNode(
                    node_id=int(getattr(node, "id")),
                    idx=int(getattr(node, "idx")),
                    price=price,
                    t=getattr(node, "t"),
                    raw_higher_than_prev=getattr(node, "higher_than_prev", None),
                    sequence_state=state,
                    sequence_valid=is_valid,
                    invalid_reason=invalid_reason,
                )
            )
            prev_price = price

        return out
