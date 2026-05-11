# NDS Core Specification v2

## Purpose

This document defines the core operating model of the Nodal Displacement Sequencing project. It converts reviewed NDS source materials into an implementation-ready structure while remaining subordinate to original NDS sources.

## Related Specification Files

See `NDS_SOURCE_ALIGNMENT_v1.md`, `NDS_TERMINOLOGY_SOURCE_GLOSSARY_v1.md`, `NDS_GEOMETRY_COMPONENTS_v1.md`, `NDS_SEQUENCE_EXECUTION_v1.md`, `NDS_123_STRUCTURES_v1.md`, `NDS_ND_NEAR_DEATH_MODEL_v1.md`, `NDS_FLAG_MODEL_v1.md`, `NDS_HOOK_GEOMETRY_v1.md`, `NDS_RALLY_GEOMETRY_v1.md`, `NDS_86_PERCENT_REFERENCE_v1.md`, `NDS_MULTI_TIMEFRAME_FRACTAL_MODEL_v1.md`, `NDS_NESTED_CYCLE_THEORY_v1.md`, `NDS_AI_ERROR_REFINEMENT_v1.md`, `NDS_MONEY_MANAGEMENT_GARCH_v1.md`, and `NDS_VISUAL_EXAMPLES_INDEX_v1.md`.

## 1. Core Principle

NDS is a source-first, node-based, cycle-based, fractal market-geometry model. It must not be reduced to swing high/low detection, generic support/resistance, raw AI prediction, single-timeframe signals, fixed Fibonacci-style levels, or hard-coded 86% rules.

## 2. Core Entities

Core entities: Node, Cycle, Trend/Rally, Pullback, Flag, Hook, ND / Near Death, 123 Structure, 86% Reference Zone, Symmetry, Fractal Timeframe Context, AI refinement layer, and GARCH risk plan.

## 3. Canonical Sequence

```text
Z -> N1 -> S1 -> N2 -> S2 -> N3 -> S3
```

N3 completes the trend-side structure. S3 completes the full cycle. A completed cycle may continue: `S3 -> N4 -> S4 -> N5 -> S5 -> N6 -> S6`.

## 4. Node Data Model

Each node should store node_id, source_label, role, cycle_id, position_in_cycle, timeframe, timestamp, raw_price, adjusted_price, OHLC values, sequence_state, flag_confirmed, nd_confirmed, hook_context, rally_context, higher_timeframe_context, symmetry_score, and source_validation_status.

## 5. Sequence State Machine

Required states: WAIT_Z, WAIT_N1, WAIT_S1, WAIT_N2, WAIT_S2, WAIT_N3, WAIT_S3, CYCLE_COMPLETE, NEXT_CYCLE, WAIT_FLAG, WAIT_POINT3_DECISION, WAIT_ND_CONFIRMATION, WAIT_HOOK_CLOSURE, WAIT_RALLY_COMPLETION, WAIT_MULTI_TIMEFRAME_CONFIRMATION, WAIT_RISK_APPROVAL.

## 6. Structural Logic

123 structures are context-specific. ND is Near Death and can form at the terminal area of any movement. Flag has SMI/BMI, Z, LVS, F components and point 3 logic. Hook has Type A and Type B in positive and negative cycles. Rally = Trend and has 123 geometry. 86% is context-specific.

## 7. Fractal Timeframe Model

Initial hierarchy: M15 -> M5 -> M1. Higher timeframes apply pressure; lower timeframes construct parent movement. Local M1 signals require M5/M15 validation.

## 8. Trend and Pullback Functions

Trend and pullback may be modeled with polynomial functions. Continuity constraints connect trend end to pullback start and pullback end to next trend start.

## 9. AI Feedback Layer

AI is an error-refinement layer over source-defined NDS structures. It must not be a raw OHLC buy/sell engine.

## 10. Risk Management

GARCH is the primary volatility and risk-management method. ATR is secondary. P_rev and P_entry are separate. Position size = Risk Amount / Stop Distance. No position reduction occurs before midpoint.

## 11. Validation Rules

Valid NDS signals must pass source-rule validation, sequence validation, node validation, flag/hook/rally context, 123 validation, ND validation if reversal is expected, symmetry validation, multi-timeframe validation, risk validation, and AI correction validation if used.

## 12. Non-Negotiable Constraints

Do not treat swing highs/lows as final NDS nodes. Do not hard-code 86%. Do not treat ND as only a flag-ending pattern. Do not merge Hook A and B. Do not use AI as NDS replacement. Do not reduce position before midpoint.
