from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional
import json

import pandas as pd

from src.python.trade_setup_builder import TradeSetup
from src.python.backtest_research import TradeEvent


@dataclass
class RunMetadata:
    run_id: str
    timestamp: pd.Timestamp
    dataset_label: str
    sequence_mode: str
    higher_timeframe_label: Optional[str] = None
    lower_timeframe_label: Optional[str] = None
    core_spec_version: Optional[str] = None
    build_version: Optional[str] = None


class ExperimentArtifactWriter:
    def setups_to_dataframe(self, setups: List[TradeSetup]) -> pd.DataFrame:
        if not setups:
            return pd.DataFrame()
        return pd.DataFrame([asdict(s) for s in setups])

    def events_to_dataframe(self, events: List[TradeEvent]) -> pd.DataFrame:
        if not events:
            return pd.DataFrame()
        return pd.DataFrame([asdict(e) for e in events])

    def write_run_metadata(self, metadata: RunMetadata, path: str | Path) -> None:
        payload = asdict(metadata)
        payload["timestamp"] = str(payload["timestamp"])
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def write_setup_ledger(self, setups: List[TradeSetup], path: str | Path) -> None:
        self.setups_to_dataframe(setups).to_csv(path, index=False)

    def write_event_ledger(self, events: List[TradeEvent], path: str | Path) -> None:
        self.events_to_dataframe(events).to_csv(path, index=False)

    def write_json_artifact(self, obj: Dict[str, Any], path: str | Path) -> None:
        def _convert(value: Any):
            if isinstance(value, pd.DataFrame):
                return value.to_dict(orient="records")
            if isinstance(value, dict):
                return {k: _convert(v) for k, v in value.items()}
            if isinstance(value, list):
                return [_convert(v) for v in value]
            return value

        Path(path).write_text(
            json.dumps(_convert(obj), indent=2, default=str),
            encoding="utf-8",
        )

    def write_full_run(
        self,
        output_dir: str | Path,
        metadata: RunMetadata,
        setups: List[TradeSetup],
        events: List[TradeEvent],
        audit: Dict[str, Any],
        analytics: Dict[str, Any],
    ) -> Dict[str, str]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        paths = {
            "run_metadata": str(output_dir / "run_metadata.json"),
            "setup_ledger": str(output_dir / "setup_ledger.csv"),
            "event_ledger": str(output_dir / "event_ledger.csv"),
            "audit_artifact": str(output_dir / "audit_artifact.json"),
            "analytics_artifact": str(output_dir / "analytics_artifact.json"),
        }

        self.write_run_metadata(metadata, paths["run_metadata"])
        self.write_setup_ledger(setups, paths["setup_ledger"])
        self.write_event_ledger(events, paths["event_ledger"])
        self.write_json_artifact(audit, paths["audit_artifact"])
        self.write_json_artifact(analytics, paths["analytics_artifact"])

        return paths
