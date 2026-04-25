from __future__ import annotations

from typing import Dict, Any, Optional

import pandas as pd

from src.python.nds_core import NDSDetector, NDSConfig
from src.python.pattern_bundle import PatternBundleBuilder
from src.python.trade_setup_builder import TradeSetupBuilder, DirectionContext
from src.python.trade_event_builder import TradeEventBuilder
from src.python.backtest_research import BacktestResearchReport
from src.python.research_audit import ResearchAuditReport
from src.python.performance_analytics import PerformanceAnalyticsReport
from src.python.multitimeframe_orchestrator import MultiTimeframeOrchestrator
from src.python.experiment_artifacts import RunMetadata, ExperimentArtifactWriter
from src.python.execution_handoff import (
    ExecutionIntent,
    ExecutionHandoffWriter,
    ExecutionHandoffMetadata,
)
from src.python.execution_policy import ExecutionPolicyEvaluator


class DeterministicBacktestPipeline:
    def __init__(self, cfg: Optional[NDSConfig] = None):
        self.cfg = cfg or NDSConfig()
        self.reporter = BacktestResearchReport()
        self.audit_reporter = ResearchAuditReport()
        self.analytics_reporter = PerformanceAnalyticsReport()
        self.artifact_writer = ExperimentArtifactWriter()
        self.execution_handoff_writer = ExecutionHandoffWriter()
        self.execution_policy_evaluator = ExecutionPolicyEvaluator()

    def run(
        self,
        df: pd.DataFrame,
        sequence_mode: str = "ascending",
        direction_context: Optional[DirectionContext] = None,
    ) -> Dict[str, Any]:
        detector = NDSDetector(df, self.cfg)

        raw_nodes = detector.detect_raw_nodes()
        sequenced_nodes = detector.classify_nodes_sequence(mode=sequence_mode)

        bundle = PatternBundleBuilder().build(sequenced_nodes)

        if direction_context is None:
            direction_context = DirectionContext(
                timestamp=pd.Timestamp(df["time"].iloc[-1]) if len(df) > 0 else pd.Timestamp.utcnow(),
                direction_owner="higher_timeframe",
                direction="long",
                is_valid=True,
                invalid_reason=None,
            )

        setups = TradeSetupBuilder().build(
            sequenced_nodes=sequenced_nodes,
            bundle=bundle,
            direction_context=direction_context,
        )
        events = TradeEventBuilder().build(df, setups)
        summary = self.reporter.build_summary(events)
        ledger = self.reporter.events_to_dataframe(events)
        audit = self.audit_reporter.build_full_audit(setups, events)
        analytics = self.analytics_reporter.build_full_analytics(setups, events)

        return {
            "raw_nodes": raw_nodes,
            "sequenced_nodes": sequenced_nodes,
            "pattern_bundle": bundle,
            "trade_setups": setups,
            "trade_events": events,
            "trade_ledger": ledger,
            "summary": summary,
            "audit": audit,
            "analytics": analytics,
        }

    def run_multitimeframe(
        self,
        higher_df: pd.DataFrame,
        lower_df: pd.DataFrame,
        higher_timeframe_label: str = "HTF",
        lower_timeframe_label: str = "LTF",
        higher_sequence_mode: str = "ascending",
        lower_sequence_mode: str = "ascending",
    ) -> Dict[str, Any]:
        higher_detector = NDSDetector(higher_df, self.cfg)
        higher_raw_nodes = higher_detector.detect_raw_nodes()
        higher_sequenced_nodes = higher_detector.classify_nodes_sequence(mode=higher_sequence_mode)

        lower_detector = NDSDetector(lower_df, self.cfg)
        lower_raw_nodes = lower_detector.detect_raw_nodes()
        lower_sequenced_nodes = lower_detector.classify_nodes_sequence(mode=lower_sequence_mode)

        orchestrator = MultiTimeframeOrchestrator()
        multiframe_context = orchestrator.build_context(
            higher_sequenced_nodes=higher_sequenced_nodes,
            lower_sequenced_nodes=lower_sequenced_nodes,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
        )
        direction_context = orchestrator.to_direction_context(multiframe_context)

        bundle = PatternBundleBuilder().build(lower_sequenced_nodes)
        setups = TradeSetupBuilder().build(
            sequenced_nodes=lower_sequenced_nodes,
            bundle=bundle,
            direction_context=direction_context,
        )
        events = TradeEventBuilder().build(lower_df, setups)
        summary = self.reporter.build_summary(events)
        ledger = self.reporter.events_to_dataframe(events)
        audit = self.audit_reporter.build_full_audit(setups, events)
        analytics = self.analytics_reporter.build_full_analytics(setups, events)

        return {
            "higher_raw_nodes": higher_raw_nodes,
            "higher_sequenced_nodes": higher_sequenced_nodes,
            "lower_raw_nodes": lower_raw_nodes,
            "lower_sequenced_nodes": lower_sequenced_nodes,
            "multiframe_context": multiframe_context,
            "pattern_bundle": bundle,
            "trade_setups": setups,
            "trade_events": events,
            "trade_ledger": ledger,
            "summary": summary,
            "audit": audit,
            "analytics": analytics,
        }

    def write_run_artifacts(
        self,
        output_dir: str,
        result: Dict[str, Any],
        run_id: str,
        dataset_label: str,
        sequence_mode: str,
        higher_timeframe_label: str | None = None,
        lower_timeframe_label: str | None = None,
        core_spec_version: str | None = None,
        build_version: str | None = None,
    ) -> Dict[str, str]:
        metadata = RunMetadata(
            run_id=run_id,
            timestamp=pd.Timestamp.utcnow(),
            dataset_label=dataset_label,
            sequence_mode=sequence_mode,
            higher_timeframe_label=higher_timeframe_label,
            lower_timeframe_label=lower_timeframe_label,
            core_spec_version=core_spec_version,
            build_version=build_version,
        )

        return self.artifact_writer.write_full_run(
            output_dir=output_dir,
            metadata=metadata,
            setups=result["trade_setups"],
            events=result["trade_events"],
            audit=result["audit"],
            analytics=result["analytics"],
        )

    def write_execution_handoff(
        self,
        output_dir: str,
        result: Dict[str, Any],
        run_id: str,
        symbol: str,
        handoff_version: str = "v1",
        source_run_metadata_path: str | None = None,
    ) -> Dict[str, str]:
        intents = self.execution_handoff_writer.setups_to_intents(
            setups=result["trade_setups"],
            symbol=symbol,
        )

        evaluated = self.execution_policy_evaluator.evaluate(intents)

        approved_like_intents = []
        for row in evaluated:
            approved_like_intents.append(
                ExecutionIntent(
                    intent_id=row.intent_id,
                    timestamp=row.timestamp,
                    symbol=row.symbol,
                    direction=row.direction,
                    entry_type=row.entry_type,
                    entry_price=row.entry_price,
                    stop_loss=row.stop_loss,
                    target=row.target,
                    source_context=row.source_context,
                    policy_state=row.policy_state,
                    is_executable=row.is_executable,
                    invalid_reason=row.block_reason or row.invalid_reason,
                )
            )

        metadata = ExecutionHandoffMetadata(
            run_id=run_id,
            timestamp=pd.Timestamp.utcnow(),
            symbol=symbol,
            handoff_version=handoff_version,
            source_run_metadata_path=source_run_metadata_path,
        )

        return self.execution_handoff_writer.write_handoff(
            output_dir=output_dir,
            intents=approved_like_intents,
            metadata=metadata,
        )
