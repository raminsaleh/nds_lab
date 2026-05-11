# NDS Prototype Detector Plan v1

## Purpose
Define the first detector-prototype plan for the NDS project.

This is not a final trading system. It is a controlled, testable prototype path.

## Core Principle
Detector development must start from structural validation, not trade execution.

Correct order:
1. Label validation
2. Sequence state machine
3. 123 / Point 3 prototype
4. ND prototype
5. 86% context engine
6. Multi-timeframe context engine
7. Flag prototype
8. Hook prototype
9. Rally prototype
10. GARCH risk approval

Invalid order:
```text
raw OHLC → indicator → buy/sell signal
```

## Detector Readiness Levels
- LEVEL_0_SPEC_ONLY
- LEVEL_1_PROTOTYPE
- LEVEL_2_LABEL_TESTED
- LEVEL_3_BACKTEST_READY
- LEVEL_4_PRODUCTION_CANDIDATE

## First Detector Priority
1. Label schema validator
2. Sequence state machine
3. 123 context classifier
4. Point 3 decision prototype
5. ND / Near Death prototype
6. 86% context engine
7. Multi-timeframe context engine
8. Flag prototype
9. Hook Type A / B prototype
10. Rally prototype
11. GARCH risk approval module

## Phase 1 — Label Schema Validator
Suggested files:
```text
nds_core/label_schema.py
nds_core/label_validation.py
tests/test_label_schema.py
```
Required checks:
- required fields exist
- label_type values are allowed
- direction is +1, -1, or 0
- confidence is valid
- source_validation_status is valid
- related_86_context is not GENERIC_86

## Phase 2 — Sequence State Machine
Canonical sequence:
```text
Z → N1 → S1 → N2 → S2 → N3 → S3
```
Invalid transitions:
- N2 before S1
- N3 before N2/S2
- S3 before N3
- CYCLE_COMPLETE at N3
- NEXT_CYCLE before S3

Suggested files:
```text
nds_core/sequence_state.py
nds_core/sequence_engine.py
tests/test_sequence_state.py
```

## Phase 3 — 123 Context Classifier
Allowed contexts:
- HOOK_CLOSURE_123
- FRACTAL_LEG_123
- RALLY_123
- TERMINAL_123
- FLAG_TERMINATION_123

Suggested files:
```text
nds_core/structures_123.py
tests/test_structures_123.py
```

## Phase 4 — Point 3 Decision Prototype
Statuses:
- REJECTED
- BROKEN
- UNRESOLVED

Routing:
```text
REJECTED → ND candidate
BROKEN → Flag continuation candidate
UNRESOLVED → wait
```
Thresholds must be configurable.

Suggested files:
```text
nds_core/point3_decision.py
tests/test_point3_decision.py
```

## Phase 5 — ND / Near Death Prototype
Required sequence:
1. terminal extreme
2. initial reversal
3. return toward prior extreme
4. failure to break prior extreme
5. rejection near reference zone
6. reversal continuation

ND must not output automatic trades.

Suggested files:
```text
nds_core/nd_near_death.py
tests/test_nd_near_death.py
```

## Phase 6 — 86% Context Engine
Allowed contexts:
- HOOK_CLOSURE
- CYCLE_CLOSURE
- POINT_Z
- ND_NEAR_RETEST
- TARGET_PROJECTION
- FLAG_HOOK_VISUAL
- RALLY_RETRACE

GENERIC_86 is invalid.

Suggested files:
```text
nds_core/reference_86.py
tests/test_reference_86.py
```

## Phase 7 — Multi-Timeframe Context Engine
Initial hierarchy:
```text
M15 → M5 → M1
```
Suggested files:
```text
nds_core/fractal_timeframes.py
nds_core/nested_cycles.py
tests/test_multitimeframe_context.py
```

## Phase 8 — Flag Prototype
Observed components:
- SMI / BMI
- Z
- LVS
- F
- internal 123
- point 3 decision

SMI/BMI/LVS/F remain source-validation-required.

## Phase 9 — Hook Type A/B Prototype
Hook A and Hook B must not be merged. Unclear cases should be HOOK_UNKNOWN.

## Phase 10 — Rally Prototype
Rally = Trend.

## Phase 11 — GARCH Risk Approval Prototype
GARCH is primary. ATR is fallback.

Risk module computes:
- sigma_t
- stop_distance
- P_stop
- risk_amount
- position_size
- P_mid
- midpoint_crossed
- trailing reduction after midpoint

P_rev ≠ P_entry.

## Detector Output Policy
Prototype detectors may output:
- candidate
- confirmed_structure
- invalid_structure
- needs_review
- confidence_score
- warnings

They must not output:
- buy
- sell
- execute_trade
- final_MT5_order

## Testing Policy
No detector should be merged without:
- one positive test
- one negative test
- one invalid-source-rule test

## No-Go Conditions
Do not proceed to full backtesting if labels are not reviewed, sequence state machine is incomplete, point 3 status is missing, ND can trigger trades directly, 86% is generic, Hook A/B are merged, M1 ignores M5/M15, or GARCH is absent.
