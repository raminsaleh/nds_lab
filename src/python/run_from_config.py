from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from src.python.node_engine import NDSConfig
from src.python.research_run_manager import ResearchRunManager


def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "time" not in df.columns:
        raise ValueError(f"Input csv must include a 'time' column: {path}")
    df["time"] = pd.to_datetime(df["time"])
    return df


def run_from_config(config: Dict[str, Any], output_dir: str | Path) -> Dict[str, Any]:
    manager = ResearchRunManager(
        NDSConfig(smoothing="none", min_distance=1, k_sigma=0.0)
    )

    mode = config["mode"]

    if mode == "single_timeframe":
        df = load_df(config["input_path"])
        return manager.rerun_single_timeframe(
            df=df,
            output_dir=output_dir,
            run_id=config["run_id"],
            dataset_label=config["dataset_label"],
            sequence_mode=config.get("sequence_mode", "ascending"),
            core_spec_version=config.get("core_spec_version"),
            build_version=config.get("build_version"),
            symbol=config.get("symbol"),
            write_execution_handoff=bool(config.get("write_execution_handoff", False)),
        )

    if mode == "multitimeframe":
        higher_df = load_df(config["higher_input_path"])
        lower_df = load_df(config["lower_input_path"])
        return manager.rerun_multitimeframe(
            higher_df=higher_df,
            lower_df=lower_df,
            output_dir=output_dir,
            run_id=config["run_id"],
            dataset_label=config["dataset_label"],
            higher_timeframe_label=config["higher_timeframe_label"],
            lower_timeframe_label=config["lower_timeframe_label"],
            higher_sequence_mode=config.get("higher_sequence_mode", "ascending"),
            lower_sequence_mode=config.get("lower_sequence_mode", "ascending"),
            core_spec_version=config.get("core_spec_version"),
            build_version=config.get("build_version"),
            symbol=config.get("symbol"),
            write_execution_handoff=bool(config.get("write_execution_handoff", False)),
        )

    raise ValueError(f"Unsupported mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run governed NDS experiment from config")
    parser.add_argument("--config", required=True, help="Path to json config")
    parser.add_argument("--output-dir", required=True, help="Directory for generated artifacts")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out = run_from_config(config, args.output_dir)

    print("Run completed.")
    print("Manifest:", out["manifest_path"])
    if out["artifact_paths"] is not None:
        for k, v in out["artifact_paths"].items():
            print(f"{k}: {v}")
    if out["handoff_paths"] is not None:
        for k, v in out["handoff_paths"].items():
            print(f"handoff::{k}: {v}")


if __name__ == "__main__":
    main()
