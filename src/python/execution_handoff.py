from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

import pandas as pd

from src.python.trade_setup_builder import TradeSetup


@dataclass
class ExecutionIntent:
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


@dataclass
class ExecutionHandoffMetadata:
    run_id: str
    timestamp: pd.Timestamp
    symbol: str
    handoff_version: str
    source_run_metadata_path: Optional[str] = None


class ExecutionHandoffWriter:
    def intents_to_dataframe(self, intents: List[ExecutionIntent]) -> pd.DataFrame:
        if not intents:
            return pd.DataFrame()
        return pd.DataFrame([asdict(i) for i in intents])

    def setups_to_intents(
        self,
        setups: List[TradeSetup],
        symbol: str,
        intent_prefix: str = "NDS_INTENT",
    ) -> List[ExecutionIntent]:
        intents: List[ExecutionIntent] = []

        for i, setup in enumerate(setups, start=1):
            intents.append(
                ExecutionIntent(
                    intent_id=f"{intent_prefix}_{i:06d}",
                    timestamp=setup.setup_time,
                    symbol=symbol,
                    direction=setup.direction,
                    entry_type="market",
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    target=setup.target,
                    source_context=setup.source_context,
                    policy_state="pending" if setup.setup_valid else "blocked",
                    is_executable=bool(setup.setup_valid),
                    invalid_reason=setup.invalid_reason,
                )
            )

        return intents

    def write_intents_csv(self, intents: List[ExecutionIntent], path: str | Path) -> None:
        self.intents_to_dataframe(intents).to_csv(path, index=False)

    def write_metadata_json(self, metadata: ExecutionHandoffMetadata, path: str | Path) -> None:
        payload = asdict(metadata)
        payload["timestamp"] = str(payload["timestamp"])
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def write_handoff(
        self,
        output_dir: str | Path,
        intents: List[ExecutionIntent],
        metadata: ExecutionHandoffMetadata,
    ) -> Dict[str, str]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        paths = {
            "execution_intents": str(output_dir / "execution_intents.csv"),
            "handoff_metadata": str(output_dir / "handoff_metadata.json"),
        }

        self.write_intents_csv(intents, paths["execution_intents"])
        self.write_metadata_json(metadata, paths["handoff_metadata"])

        return paths
