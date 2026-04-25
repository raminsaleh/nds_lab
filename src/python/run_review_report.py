from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class RunReviewReportBuilder:
    def _load_json(self, path: str | Path) -> Dict[str, Any]:
        return json.loads(Path(path).read_text(encoding="utf-8"))

    def build_review(
        self,
        manifest_path: str | Path,
        analytics_path: str | Path,
        audit_path: str | Path,
        handoff_metadata_path: str | Path | None = None,
    ) -> Dict[str, Any]:
        manifest = self._load_json(manifest_path)
        analytics = self._load_json(analytics_path)
        audit = self._load_json(audit_path)
        handoff = self._load_json(handoff_metadata_path) if handoff_metadata_path else None

        summary_metrics = analytics.get("summary_metrics", {})
        path_metrics = analytics.get("path_metrics", {})
        streak_metrics = analytics.get("streak_metrics", {})

        review = {
            "run_id": manifest.get("run_id"),
            "dataset_label": manifest.get("dataset_label"),
            "sequence_mode": manifest.get("sequence_mode"),
            "higher_timeframe_label": manifest.get("higher_timeframe_label"),
            "lower_timeframe_label": manifest.get("lower_timeframe_label"),
            "core_spec_version": manifest.get("core_spec_version"),
            "build_version": manifest.get("build_version"),
            "summary_metrics": summary_metrics,
            "path_metrics": path_metrics,
            "streak_metrics": streak_metrics,
            "failure_buckets": audit.get("failure_buckets", {}),
            "invalidation_buckets": audit.get("invalidation_buckets", {}),
            "source_context_buckets": audit.get("source_context_buckets", {}),
            "event_outcome_buckets": audit.get("event_outcome_buckets", {}),
            "execution_handoff_present": handoff is not None,
        }

        return review

    def write_review_json(self, review: Dict[str, Any], path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(review, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    def write_review_markdown(self, review: Dict[str, Any], path: str | Path) -> None:
        content = f"""# Run Review

Run ID: `{review.get("run_id")}`
Dataset: `{review.get("dataset_label")}`
Sequence mode: `{review.get("sequence_mode")}`
Higher timeframe: `{review.get("higher_timeframe_label")}`
Lower timeframe: `{review.get("lower_timeframe_label")}`
Core spec version: `{review.get("core_spec_version")}`
Build version: `{review.get("build_version")}`

## Summary Metrics
- trade_count: {review.get("summary_metrics", {}).get("trade_count")}
- win_rate: {review.get("summary_metrics", {}).get("win_rate")}
- expectancy_points: {review.get("summary_metrics", {}).get("expectancy_points")}
- total_points: {review.get("summary_metrics", {}).get("total_points")}
- total_r: {review.get("summary_metrics", {}).get("total_r")}

## Path Metrics
- max_drawdown_points: {review.get("path_metrics", {}).get("max_drawdown_points")}

## Streak Metrics
- max_win_streak: {review.get("streak_metrics", {}).get("max_win_streak")}
- max_loss_streak: {review.get("streak_metrics", {}).get("max_loss_streak")}
- current_streak_type: {review.get("streak_metrics", {}).get("current_streak_type")}
- current_streak_length: {review.get("streak_metrics", {}).get("current_streak_length")}

## Failure Buckets
{json.dumps(review.get("failure_buckets", {}), indent=2, ensure_ascii=False)}

## Invalidation Buckets
{json.dumps(review.get("invalidation_buckets", {}), indent=2, ensure_ascii=False)}

## Source Context Buckets
{json.dumps(review.get("source_context_buckets", {}), indent=2, ensure_ascii=False)}

## Event Outcome Buckets
{json.dumps(review.get("event_outcome_buckets", {}), indent=2, ensure_ascii=False)}

## Execution Handoff
- present: {review.get("execution_handoff_present")}
"""
        Path(path).write_text(content, encoding="utf-8")
