# NDS Template Library v1

## Purpose
Define the initial structural template library for NDS. Templates are source-aligned blueprints, not final detector code.

## Core Principle
Templates must be derived from original NDS sources, visual examples, source-aligned specs, and manually labeled US30 data. Do not create templates from generic chart-pattern assumptions.

## Template Status Levels
- TEMPLATE_DRAFT
- TEMPLATE_VISUALLY_REVIEWED
- TEMPLATE_LABEL_TESTED
- TEMPLATE_BACKTEST_READY
- TEMPLATE_REJECTED

## Template Data Model
```text
NDSTemplate:
  template_id
  template_name
  component_type
  direction
  source_files
  related_specs
  required_points
  optional_points
  required_sequence_context
  required_timeframe_context
  required_geometry_checks
  required_symmetry_checks
  related_86_context
  point3_logic
  nd_logic
  flag_logic
  hook_logic
  validation_status
  open_questions
  notes
```

## Core Templates
1. TPL_CYCLE_CANONICAL_v1
2. TPL_NODE_SEQUENCE_v1
3. TPL_123_CONTEXTUAL_v1
4. TPL_POINT3_DECISION_v1
5. TPL_ND_NEAR_DEATH_v1
6. TPL_FLAG_CONTEXTUAL_v1
7. TPL_HOOK_TYPE_A_v1
8. TPL_HOOK_TYPE_B_v1
9. TPL_RALLY_TREND_v1
10. TPL_86_CONTEXTUAL_REFERENCE_v1
11. TPL_MULTITIMEFRAME_PARENT_CHILD_v1

## Cycle Template
Canonical structure:
```text
Z → N1 → S1 → N2 → S2 → N3 → S3
```
N3 is trend-side completion. S3 is full cycle completion.

Invalid:
- cycle complete at N3
- skipped S nodes
- generic swing nodes

## 123 Template
Allowed contexts:
- HOOK_CLOSURE_123
- FRACTAL_LEG_123
- RALLY_123
- TERMINAL_123
- FLAG_TERMINATION_123

Generic 123 detection is invalid.

## Point 3 Decision Template
Statuses:
- REJECTED
- BROKEN
- UNRESOLVED

Decision logic:
```text
REJECTED → evaluate ND
BROKEN → evaluate Flag continuation toward F
UNRESOLVED → wait
```

## ND / Near Death Template
Required sequence:
1. terminal extreme
2. initial reversal
3. return toward prior extreme
4. failure to break prior extreme
5. rejection near reference zone
6. reversal continuation

ND is not limited to flag endings and must not create automatic trades.

## Flag Template
Observed components:
- SMI / BMI
- Z
- LVS
- F
- internal 123
- point 3 decision

Flag is not generic consolidation.

## Hook Type A Template
Required checks:
- cycle polarity
- direction
- related 123
- X-axis geometry
- Y-axis geometry
- symmetry
- related 86%
- possible ND
- parent timeframe

## Hook Type B Template
Hook B must remain separate from Hook A. Exact relationship to flags and closure behavior is SOURCE_VALIDATION_REQUIRED.

## Rally / Trend Template
In NDS:
```text
Rally = Trend
```
A rally may contain segment 1, segment 2, segment 3, point 3 decision, symmetry, exhaustion, continuation, or ND scenario.

## 86% Reference Template
Allowed contexts:
- HOOK_CLOSURE
- CYCLE_CLOSURE
- POINT_Z
- ND_NEAR_RETEST
- TARGET_PROJECTION
- FLAG_HOOK_VISUAL
- RALLY_RETRACE

GENERIC_86 is invalid.

## Multi-Timeframe Template
Initial hierarchy:
```text
M15 → M5 → M1
```
Mapping:
```text
M15 parent structure → M5 child structures → M1 microstructure / trigger candidate
```

## Template-to-Detector Mapping
| Template | Future detector |
|---|---|
| TPL_CYCLE_CANONICAL_v1 | `detect_cycle()` |
| TPL_NODE_SEQUENCE_v1 | `update_sequence_state()` |
| TPL_123_CONTEXTUAL_v1 | `detect_123_context()` |
| TPL_POINT3_DECISION_v1 | `evaluate_point3_decision()` |
| TPL_ND_NEAR_DEATH_v1 | `detect_nd_near_death()` |
| TPL_FLAG_CONTEXTUAL_v1 | `detect_flag()` |
| TPL_HOOK_TYPE_A_v1 | `detect_hook_type_a()` |
| TPL_HOOK_TYPE_B_v1 | `detect_hook_type_b()` |
| TPL_RALLY_TREND_v1 | `detect_rally()` |
| TPL_86_CONTEXTUAL_REFERENCE_v1 | `compute_86_reference()` |
| TPL_MULTITIMEFRAME_PARENT_CHILD_v1 | `evaluate_multitimeframe_context()` |

## Invalid Uses
Do not treat templates as final code, merge Hook A/B, use generic 123 or generic 86%, label all consolidations as Flag, label all pullbacks as Hook, or ignore parent timeframe context.
