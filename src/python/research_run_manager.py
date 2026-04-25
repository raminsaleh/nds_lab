from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, Optional
import json

import pandas as pd

from src.python.deterministic_backtest_pipeline import DeterministicBacktestPipeline
from src.python.node_engine import NDSConfig


@dataclass
class RunManifest:
    run_id: str
    dataset_label: str
    sequence_mode: str
    higher_timeframe_label: Optional[str]
    lower_timeframe_label: Optional[str]
    core_spec_version: Optional[str]
    build_version: Optional[str]
    generated_paths: Dict[str, str]


class ResearchRunManager:
    def __init__(self, cfg: Optional[NDSConfig] = None):
        self.pipeline = DeterministicBacktestPipeline(cfg or NDSConfig())

    def rerun_single_timeframe(
        self,
        df: pd.DataFrame,
        output_dir: str | Path,
        run_id: str,
        dataset_label: str,
        sequence_mode: str = "ascending",
        core_spec_version: Optional[str] = None,
        build_version: Optional[str] = None,
        symbol: Optional[str] = None,
        write_execution_handoff: bool = False,
    ) -> Dict[str, Any]:
        result = self.pipeline.run(df=df, sequence_mode=sequence_mode)

        artifact_paths = self.pipeline.write_run_artifacts(
            output_dir=str(output_dir),
            result=result,
            run_id=run_id,
            dataset_label=dataset_label,
            sequence_mode=sequence_mode,
            core_spec_version=core_spec_version,
            build_version=build_version,
        )

        handoff_paths = None
        if write_execution_handoff and symbol is not None:
            handoff_paths = self.pipeline.write_execution_handoff(
                output_dir=str(Path(output_dir) / "execution_handoff"),
                result=result,
                run_id=run_id,
                symbol=symbol,
                source_run_metadata_path=artifact_paths["run_metadata"],
            )

        manifest = RunManifest(
            run_id=run_id,
            dataset_label=dataset_label,
            sequence_mode=sequence_mode,
            higher_timeframe_label=None,
            lower_timeframe_label=None,
            core_spec_version=core_spec_version,
            build_version=build_version,
            generated_paths={
                **artifact_paths,
                **({f"handoff::{k}": v for k, v in handoff_paths.items()} if handoff_paths else {}),
            },
        )

        manifest_path = self._write_manifest(output_dir, manifest)

        return {
            "result": result,
            "artifact_paths": artifact_paths,
            "handoff_paths": handoff_paths,
            "manifest": manifest,
            "manifest_path": manifest_path,
        }

    def rerun_multitimeframe(
        self,
        higher_df: pd.DataFrame,
        lower_df: pd.DataFrame,
        output_dir: str | Path,
        run_id: str,
        dataset_label: str,
        higher_timeframe_label: str,
        lower_timeframe_label: str,
        higher_sequence_mode: str = "ascending",
        lower_sequence_mode: str = "ascending",
        core_spec_version: Optional[str] = None,
        build_version: Optional[str] = None,
        symbol: Optional[str] = None,
        write_execution_handoff: bool = False,
    ) -> Dict[str, Any]:
        result = self.pipeline.run_multitimeframe(
            higher_df=higher_df,
            lower_df=lower_df,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
            higher_sequence_mode=higher_sequence_mode,
            lower_sequence_mode=lower_sequence_mode,
        )

        artifact_paths = self.pipeline.write_run_artifacts(
            output_dir=str(output_dir),
            result=result,
            run_id=run_id,
            dataset_label=dataset_label,
            sequence_mode=lower_sequence_mode,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
            core_spec_version=core_spec_version,
            build_version=build_version,
        )

        handoff_paths = None
        if write_execution_handoff and symbol is not None:
            handoff_paths = self.pipeline.write_execution_handoff(
                output_dir=str(Path(output_dir) / "execution_handoff"),
                result=result,
                run_id=run_id,
                symbol=symbol,
                source_run_metadata_path=artifact_paths["run_metadata"],
            )

        manifest = RunManifest(
            run_id=run_id,
            dataset_label=dataset_label,
            sequence_mode=lower_sequence_mode,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
            core_spec_version=core_spec_version,
            build_version=build_version,
            generated_paths={
                **artifact_paths,
                **({f"handoff::{k}": v for k, v in handoff_paths.items()} if handoff_paths else {}),
            },
        )

        manifest_path = self._write_manifest(output_dir, manifest)

        return {
            "result": result,
            "artifact_paths": artifact_paths,
            "handoff_paths": handoff_paths,
            "manifest": manifest,
            "manifest_path": manifest_path,
        }

    def _write_manifest(self, output_dir: str | Path, manifest: RunManifest) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "run_manifest.json"
        path.write_text(json.dumps(asdict(manifest), indent=2, default=str), encoding="utf-8")
        return str(path)
