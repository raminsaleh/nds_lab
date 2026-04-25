from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class HookPattern:
    hook_id: int
    start_node_id: int
    end_node_id: int
    sequence_context: str
    cycle_position_context: str
    polarity: str
    symmetry_context: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None


@dataclass
class Pattern123:
    pattern_id: int
    anchor_node_ids: List[int]
    sequence_context: str
    rally_context: str
    role_context: str
    flag_relation: str
    hook_relation: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None


@dataclass
class FlagPattern:
    flag_id: int
    anchor_node_ids: List[int]
    sequence_context: str
    rally_context: str
    terminal_cycle_context: str
    hook_relation: str
    pattern_123_relation: str
    smi_context: str
    low_volume_spike_context: str
    is_valid: bool = True
    invalid_reason: Optional[str] = None


@dataclass
class PatternBundle:
    hooks: List[HookPattern]
    patterns_123: List[Pattern123]
    flags: List[FlagPattern]


class PatternBundleBuilder:
    """
    First governed scaffold for bundling Hook / 123 / Flag outputs from
    sequenced nodes.
    """

    def build(self, sequenced_nodes: List[object]) -> PatternBundle:
        hooks = self._build_hooks(sequenced_nodes)
        patterns_123 = self._build_123(sequenced_nodes, hooks)
        flags = self._build_flags(sequenced_nodes, hooks, patterns_123)
        return PatternBundle(hooks=hooks, patterns_123=patterns_123, flags=flags)

    def _build_hooks(self, sequenced_nodes: List[object]) -> List[HookPattern]:
        hooks: List[HookPattern] = []
        hook_id = 1
        for i in range(len(sequenced_nodes) - 1):
            a = sequenced_nodes[i]
            b = sequenced_nodes[i + 1]
            hooks.append(
                HookPattern(
                    hook_id=hook_id,
                    start_node_id=int(getattr(a, "node_id")),
                    end_node_id=int(getattr(b, "node_id")),
                    sequence_context=f"{getattr(getattr(a, 'sequence_state', None), 'value', '')}->{getattr(getattr(b, 'sequence_state', None), 'value', '')}",
                    cycle_position_context="scaffold",
                    polarity="up" if float(getattr(b, "price")) >= float(getattr(a, "price")) else "down",
                    symmetry_context="scaffold",
                    is_valid=bool(getattr(a, "sequence_valid", False) and getattr(b, "sequence_valid", False)),
                    invalid_reason=None,
                )
            )
            hook_id += 1
        return hooks

    def _build_123(self, sequenced_nodes: List[object], hooks: List[HookPattern]) -> List[Pattern123]:
        patterns: List[Pattern123] = []
        pid = 1
        for i in range(len(sequenced_nodes) - 2):
            triad = sequenced_nodes[i : i + 3]
            valid = all(bool(getattr(x, "sequence_valid", False)) for x in triad)
            patterns.append(
                Pattern123(
                    pattern_id=pid,
                    anchor_node_ids=[int(getattr(x, "node_id")) for x in triad],
                    sequence_context="/".join(getattr(getattr(x, "sequence_state", None), "value", "") for x in triad),
                    rally_context="scaffold",
                    role_context="scaffold",
                    flag_relation="scaffold",
                    hook_relation="scaffold",
                    is_valid=valid,
                    invalid_reason=None if valid else "invalid_sequence_member",
                )
            )
            pid += 1
        return patterns

    def _build_flags(
        self,
        sequenced_nodes: List[object],
        hooks: List[HookPattern],
        patterns_123: List[Pattern123],
    ) -> List[FlagPattern]:
        flags: List[FlagPattern] = []
        fid = 1
        for i in range(0, max(0, len(sequenced_nodes) - 3), 2):
            block = sequenced_nodes[i : i + 4]
            if len(block) < 4:
                continue
            valid = all(bool(getattr(x, "sequence_valid", False)) for x in block)
            flags.append(
                FlagPattern(
                    flag_id=fid,
                    anchor_node_ids=[int(getattr(x, "node_id")) for x in block],
                    sequence_context="/".join(getattr(getattr(x, "sequence_state", None), "value", "") for x in block),
                    rally_context="scaffold",
                    terminal_cycle_context="scaffold",
                    hook_relation="scaffold",
                    pattern_123_relation="scaffold",
                    smi_context="scaffold",
                    low_volume_spike_context="scaffold",
                    is_valid=valid,
                    invalid_reason=None if valid else "invalid_sequence_member",
                )
            )
            fid += 1
        return flags
