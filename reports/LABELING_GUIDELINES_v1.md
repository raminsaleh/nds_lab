# NDS Labeling Guidelines v1

## Purpose
Define manual-labeling rules for NDS structures on real US30 market data.

## Core Rule
Do not label generic swing highs/lows as final NDS nodes. A valid NDS label must consider sequence context, timeframe context, 123 structure, flag/hook/ND context, 86% context, symmetry, and higher-timeframe pressure.

## Initial Scope
- Instrument: US30 / Dow Jones
- Hierarchy: M15 → M5 → M1
- First sample: clean overlapping 2-4 week window with visible trend, pullback, consolidation, and reversal behavior.

## Required Label Types
- Z
- N1 / S1 / N2 / S2 / N3 / S3
- Cycle
- 123 structure
- Point 3
- ND / Near Death
- Flag
- Hook Type A / Hook Type B / Hook Unknown
- Rally / Trend
- 86% reference context
- Parent / child timeframe relation

## Confidence
Allowed:
- CONFIRMED
- PROBABLE
- UNCERTAIN
- REQUIRES_REVIEW

Do not train detectors on UNCERTAIN or REQUIRES_REVIEW labels unless testing ambiguity.

## Source Validation Status
Allowed:
- SOURCE_CONFIRMED
- SOURCE_COMPATIBLE_INTERPRETATION
- SOURCE_VALIDATION_REQUIRED

## CSV Fields
```text
label_id,symbol,timeframe,timestamp_start,timestamp_end,price_start,price_end,label_type,direction,cycle_id,parent_label_id,child_label_ids,confidence,source_validation_status,related_86_context,related_point3_status,notes
```

## Label Rules
### Z
Must be justified by NDS structure, not only a high or low.

### N/S Nodes
Follow sequence:
```text
Z → N1 → S1 → N2 → S2 → N3 → S3
```
N3 is trend-side completion. S3 may complete the full cycle.

### 123
Must be context-classified:
- HOOK_CLOSURE_123
- FRACTAL_LEG_123
- RALLY_123
- TERMINAL_123
- FLAG_TERMINATION_123

### Point 3
Allowed statuses:
- REJECTED
- BROKEN
- UNRESOLVED

Point 3 rejected → evaluate ND. Point 3 broken → evaluate Flag continuation toward F.

### ND / Near Death
Required structure:
1. terminal extreme
2. initial reversal
3. return toward prior extreme
4. failure to break prior extreme
5. rejection near reference zone
6. reversal continuation

### 86%
Allowed contexts:
- HOOK_CLOSURE
- CYCLE_CLOSURE
- POINT_Z
- ND_NEAR_RETEST
- TARGET_PROJECTION
- FLAG_HOOK_VISUAL
- RALLY_RETRACE

GENERIC_86 is invalid.

## Workflow
1. Select clean overlapping M15/M5/M1 window.
2. Label M15 first.
3. Label child M5 structures.
4. Label M1 microstructure / ND candidates.
5. Assign confidence and source validation.
6. Review labels before detector work.
