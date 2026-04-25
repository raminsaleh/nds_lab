from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any
import json


@dataclass
class RunComparison:
    base_run_id: str
    candidate_run_id: str
    trade_count_delta: int
    win_rate_delta: float
    expectancy_points_delta: float
    total_points_delta: float
    total_r_delta: float
    max_drawdown_points_delta: float


class RunComparisonBuilder:
    def load_json(self, path: str | Path) -> Dict[str, Any]:
        return json.loads(Path(path).read_text(encoding="utf-8"))

    def compare_analytics_artifacts(
        self,
        base_analytics_path: str | Path,
        candidate_analytics_path: str | Path,
        base_run_id: str,
        candidate_run_id: str,
    ) -> RunComparison:
        base = self.load_json(base_analytics_path)
        cand = self.load_json(candidate_analytics_path)

        base_summary = base.get("summary_metrics", {})
        cand_summary = cand.get("summary_metrics", {})

        base_path = base.get("path_metrics", {})
        cand_path = cand.get("path_metrics", {})

        return RunComparison(
            base_run_id=base_run_id,
            candidate_run_id=candidate_run_id,
            trade_count_delta=int(cand_summary.get("trade_count", 0)) - int(base_summary.get("trade_count", 0)),
            win_rate_delta=float(cand_summary.get("win_rate", 0.0)) - float(base_summary.get("win_rate", 0.0)),
            expectancy_points_delta=float(cand_summary.get("expectancy_points", 0.0)) - float(base_summary.get("expectancy_points", 0.0)),
            total_points_delta=float(cand_summary.get("total_points", 0.0)) - float(base_summary.get("total_points", 0.0)),
            total_r_delta=float(cand_summary.get("total_r", 0.0)) - float(base_summary.get("total_r", 0.0)),
            max_drawdown_points_delta=float(cand_path.get("max_drawdown_points", 0.0)) - float(base_path.get("max_drawdown_points", 0.0)),
        )

    def write_comparison_json(
        self,
        comparison: RunComparison,
        path: str | Path,
    ) -> None:
        Path(path).write_text(
            json.dumps(asdict(comparison), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def write_comparison_markdown(
        self,
        comparison: RunComparison,
        path: str | Path,
    ) -> None:
        content = f"""# Run Comparison

Base run: `{comparison.base_run_id}`
Candidate run: `{comparison.candidate_run_id}`

- trade_count_delta: {comparison.trade_count_delta}
- win_rate_delta: {comparison.win_rate_delta}
- expectancy_points_delta: {comparison.expectancy_points_delta}
- total_points_delta: {comparison.total_points_delta}
- total_r_delta: {comparison.total_r_delta}
- max_drawdown_points_delta: {comparison.max_drawdown_points_delta}
"""
        Path(path).write_text(content, encoding="utf-8")
