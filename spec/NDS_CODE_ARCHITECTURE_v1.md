# NDS Code Architecture v1

## Purpose
Define the proposed software architecture for the NDS project.

This document does not define final detector logic. It defines a clean, modular, testable implementation structure.

## Core Flow
Correct:
```text
Data → Labels → Core Models → Sequence Engine → Structural Detectors → Multi-Timeframe Context → AI Refinement → GARCH Risk Approval → Backtest → MT5 Export
```

Invalid:
```text
Raw OHLC → Indicator → Buy/Sell
```

## Proposed Repository Structure
```text
nds_lab/
  spec/
  reports/
  data/
  nds_core/
  nds_risk/
  nds_ai/
  backtests/
  mt5/
  tests/
  scripts/
```

## nds_core/
Recommended modules:
```text
nds_core/
  __init__.py
  enums.py
  models.py
  label_schema.py
  label_validation.py
  sequence_state.py
  sequence_engine.py
  structures_123.py
  point3_decision.py
  nd_near_death.py
  flag_model.py
  hook_geometry.py
  rally_geometry.py
  reference_86.py
  fractal_timeframes.py
  nested_cycles.py
  symmetry.py
  validation.py
```

## Core Modules
### enums.py
Defines allowed values:
- Timeframe
- Direction
- LabelType
- ConfidenceLevel
- SourceValidationStatus
- Point3Status
- CandidateStatus
- HookType
- CyclePolarity
- Reference86Context

### models.py
Defines:
- NDSLabel
- NDSNode
- NDSCycle
- NDS123Structure
- NDSNearDeathCandidate
- NDSFlagCandidate
- NDSHookCandidate
- NDSRallyCandidate
- NDS86Reference
- NDSMultiTimeframeContext
- NDSDetectorResult

Models store structure. They should not contain heavy detector logic.

### label_schema.py
Implements `spec/NDS_LABEL_SCHEMA_v1.md`.

### label_validation.py
Validates manual label files before detectors use them.

### sequence_state.py
Defines sequence states:
- WAIT_Z
- WAIT_N1
- WAIT_S1
- WAIT_N2
- WAIT_S2
- WAIT_N3
- WAIT_S3
- CYCLE_COMPLETE
- NEXT_CYCLE
- WAIT_POINT3_DECISION
- WAIT_ND_CONFIRMATION
- WAIT_FLAG
- WAIT_MULTI_TIMEFRAME_CONFIRMATION
- WAIT_RISK_APPROVAL

### sequence_engine.py
Implements legal state transitions:
```text
Z → N1 → S1 → N2 → S2 → N3 → S3
```

### structures_123.py
Contextual 123 classification. Generic 123 is invalid.

### point3_decision.py
Evaluates REJECTED / BROKEN / UNRESOLVED. Thresholds must be configurable.

### nd_near_death.py
Prototype ND / Near Death detector. ND can create a trigger candidate, not an automatic trade.

### reference_86.py
Context-aware 86% reference engine. GENERIC_86 is invalid.

### fractal_timeframes.py
Handles M15 → M5 → M1 hierarchy.

### nested_cycles.py
Handles parent/child cycles, raw vs adjusted nodes, higher-timeframe pressure, and local conflict downgrade.

### symmetry.py
Computes symmetry scores for 123, Hook, Rally, Cycle, and node displacement.

## nds_risk/
Recommended modules:
```text
nds_risk/
  __init__.py
  garch_volatility.py
  atr_volatility.py
  position_sizing.py
  midpoint_trailing.py
  broker_point_value.py
  risk_plan.py
```

Rules:
- GARCH is primary.
- ATR is fallback.
- Position size must use risk amount, stop distance, and point value.
- No position reduction before midpoint.

## nds_ai/
Recommended modules:
```text
nds_ai/
  __init__.py
  polynomial_fit.py
  residuals.py
  random_forest_residual.py
  neural_residual.py
  model_validation.py
  feature_engineering.py
```

AI must not be a direct trade engine.

Valid:
```text
NDS structure → residuals → AI correction → source-rule validation
```

Invalid:
```text
raw OHLC → AI → buy/sell
```

## backtests/
Recommended modules:
```text
backtests/
  run_structure_backtest.py
  run_risk_backtest.py
  run_full_strategy_backtest.py
  backtest_engine.py
  metrics.py
```

Backtest stages:
1. Structure-only backtest
2. Sequence validation backtest
3. ND trigger validation
4. GARCH risk simulation
5. Full trade simulation

## mt5/
Recommended:
```text
mt5/
  export_nds_signals.py
  export_risk_plan.py
  NDS_EA_SPEC_v1.md
```

MT5 should receive only validated trade candidates and risk plans. EA must not override NDS context or GARCH risk.

## tests/
Recommended tests:
```text
tests/
  test_label_schema.py
  test_label_validation.py
  test_sequence_state.py
  test_sequence_engine.py
  test_structures_123.py
  test_point3_decision.py
  test_nd_near_death.py
  test_reference_86.py
  test_multitimeframe_context.py
  test_hook_geometry.py
  test_rally_geometry.py
  test_garch_risk.py
```

Minimum testing rule:
No detector module should be accepted without one positive test, one negative test, and one invalid-source-rule test.

## Shared Detector Result
```text
NDSDetectorResult:
  detector_name
  component_type
  timeframe
  direction
  candidate_status
  confidence_score
  source_validation_status
  related_labels
  related_parent_context
  related_86_context
  warnings
  notes
```

Allowed candidate statuses:
- CANDIDATE
- CONFIRMED_STRUCTURE
- INVALID_STRUCTURE
- NEEDS_REVIEW
- AGAINST_PARENT_PRESSURE
- INSUFFICIENT_DATA

## Development Order
1. `nds_core/enums.py`
2. `nds_core/models.py`
3. `nds_core/label_schema.py`
4. `nds_core/label_validation.py`
5. `nds_core/sequence_state.py`
6. `nds_core/sequence_engine.py`
7. `tests/test_label_schema.py`
8. `tests/test_sequence_state.py`
9. `nds_core/structures_123.py`
10. `nds_core/point3_decision.py`
11. `nds_core/nd_near_death.py`
12. `nds_core/reference_86.py`
13. `nds_core/fractal_timeframes.py`
14. `nds_core/nested_cycles.py`
15. `nds_risk/garch_volatility.py`

## No-Go Conditions
Do not implement final detectors if labels do not exist, label validation is not implemented, sequence state machine is missing, 86% context is generic, point 3 thresholds are hard-coded, ND can trigger trades directly, GARCH is missing, or M1/M5/M15 context is ignored.
