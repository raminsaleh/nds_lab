# NDS Label Schema v1

## Purpose
Define the official label schema for manually labeling NDS structures on real market data.

## Main Label Object
```text
NDSLabel:
  label_id
  symbol
  timeframe
  timestamp_start
  timestamp_end
  price_start
  price_end
  label_type
  direction
  cycle_id
  parent_label_id
  child_label_ids
  confidence
  source_validation_status
  related_86_context
  related_point3_status
  related_flag_id
  related_hook_id
  related_nd_id
  related_rally_id
  notes
```

## Required Fields
- label_id
- symbol
- timeframe
- timestamp_start
- label_type
- direction
- confidence
- source_validation_status

## Allowed Label Types
### Nodes
- Z
- N1
- S1
- N2
- S2
- N3
- S3

### Cycle
- CYCLE
- CYCLE_START
- CYCLE_END
- CYCLE_CLOSURE

### 123
- STRUCTURE_123
- HOOK_CLOSURE_123
- FRACTAL_LEG_123
- RALLY_123
- TERMINAL_123
- FLAG_TERMINATION_123
- POINT_1
- POINT_2
- POINT_3

### ND
- ND_CANDIDATE
- ND_CONFIRMED
- ND_INVALIDATED

### Flag
- FLAG_CANDIDATE
- FLAG_CONFIRMED
- FLAG_INVALIDATED
- SMI
- BMI
- LVS
- F

### Hook
- HOOK_CANDIDATE
- HOOK_TYPE_A
- HOOK_TYPE_B
- HOOK_UNKNOWN
- HOOK_CLOSURE

### Rally
- RALLY
- RALLY_SEGMENT_1
- RALLY_SEGMENT_2
- RALLY_SEGMENT_3
- RALLY_COMPLETION
- RALLY_EXHAUSTION

### 86%
- REFERENCE_86
- HOOK_CLOSURE_86
- CYCLE_CLOSURE_86
- POINT_Z_86
- ND_RETEST_86
- TARGET_PROJECTION_86
- FLAG_HOOK_VISUAL_86
- RALLY_RETRACE_86

## Direction
- +1 = bullish / upward normalized
- -1 = bearish / downward normalized
- 0 = neutral / unresolved

## Confidence
- CONFIRMED
- PROBABLE
- UNCERTAIN
- REQUIRES_REVIEW

## Source Validation Status
- SOURCE_CONFIRMED
- SOURCE_COMPATIBLE_INTERPRETATION
- SOURCE_VALIDATION_REQUIRED

## Point 3 Status
- REJECTED
- BROKEN
- UNRESOLVED
- NOT_APPLICABLE

## 86% Context
- HOOK_CLOSURE
- CYCLE_CLOSURE
- POINT_Z
- ND_NEAR_RETEST
- TARGET_PROJECTION
- FLAG_HOOK_VISUAL
- RALLY_RETRACE
- NOT_APPLICABLE

GENERIC_86 is not allowed.

## CSV Schema
```text
label_id,symbol,timeframe,timestamp_start,timestamp_end,price_start,price_end,label_type,direction,cycle_id,parent_label_id,child_label_ids,confidence,source_validation_status,related_86_context,related_point3_status,related_flag_id,related_hook_id,related_nd_id,related_rally_id,notes
```

## JSON Example
```json
{
  "label_id": "LBL_000001",
  "symbol": "US30",
  "timeframe": "M15",
  "timestamp_start": "2026-01-05 09:00",
  "timestamp_end": "2026-01-05 09:00",
  "price_start": 37650.0,
  "price_end": 37650.0,
  "label_type": "Z",
  "direction": 1,
  "cycle_id": "CYCLE_0001",
  "parent_label_id": null,
  "child_label_ids": [],
  "confidence": "PROBABLE",
  "source_validation_status": "SOURCE_COMPATIBLE_INTERPRETATION",
  "related_86_context": "POINT_Z",
  "related_point3_status": "NOT_APPLICABLE",
  "notes": "Initial Z candidate"
}
```

## Validation Rules
A label is invalid if required fields are missing, direction is not +1/-1/0, confidence is missing, source_validation_status is missing, or related_86_context is GENERIC_86.

## File Naming
```text
data/labels/US30_M15_labels_v1.csv
data/labels/US30_M5_labels_v1.csv
data/labels/US30_M1_labels_v1.csv
```
