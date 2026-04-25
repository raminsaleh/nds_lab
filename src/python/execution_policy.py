from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from src.python.execution_handoff import ExecutionIntent


@dataclass
class PolicyEvaluatedIntent:
    intent_id: str
    timestamp: pd.Timestamp
    symbol: str
    direction: str
    entry_type: str
    entry_price: float
    stop_loss: float
    target: float
    source_context: str
    policy_state: str
    is_executable: bool
    invalid_reason: Optional[str] = None
    block_reason: Optional[str] = None


class ExecutionPolicyEvaluator:
    def evaluate(self, intents: List[ExecutionIntent]) -> List[PolicyEvaluatedIntent]:
        out: List[PolicyEvaluatedIntent] = []

        for intent in intents:
            block_reason = None
            policy_state = intent.policy_state
            is_executable = intent.is_executable
            invalid_reason = intent.invalid_reason

            if intent.direction not in {"long", "short"}:
                policy_state = "blocked"
                is_executable = False
                block_reason = "invalid_direction"

            elif intent.entry_price == 0 or intent.stop_loss == 0 or intent.target == 0:
                policy_state = "blocked"
                is_executable = False
                block_reason = "zero_price_field"

            elif not intent.is_executable:
                policy_state = "blocked"
                is_executable = False
                block_reason = intent.invalid_reason or "intent_not_executable"

            else:
                policy_state = "approved"
                is_executable = True

            out.append(
                PolicyEvaluatedIntent(
                    intent_id=intent.intent_id,
                    timestamp=intent.timestamp,
                    symbol=intent.symbol,
                    direction=intent.direction,
                    entry_type=intent.entry_type,
                    entry_price=intent.entry_price,
                    stop_loss=intent.stop_loss,
                    target=intent.target,
                    source_context=intent.source_context,
                    policy_state=policy_state,
                    is_executable=is_executable,
                    invalid_reason=invalid_reason,
                    block_reason=block_reason,
                )
            )

        return out
