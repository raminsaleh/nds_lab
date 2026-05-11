# NDS Labeling Review v1

## Purpose
Review the first manually labeled NDS sample window before detector development.

## Review Scope
- Instrument: US30 / Dow Jones
- Timeframes: M15, M5, M1
- Sample start: TBD
- Sample end: TBD
- Data source: TBD
- Timezone: TBD

## Input Label Files
| Timeframe | Label file | Status |
|---|---|---|
| M15 | `data/labels/US30_M15_labels_v1.csv` | PENDING |
| M5 | `data/labels/US30_M5_labels_v1.csv` | PENDING |
| M1 | `data/labels/US30_M1_labels_v1.csv` | PENDING |

## Required Label Coverage
| Label type | Present? | Count | Confidence | Notes |
|---|---|---:|---|---|
| Z | TBD | TBD | TBD | TBD |
| N/S nodes | TBD | TBD | TBD | TBD |
| Cycle | TBD | TBD | TBD | TBD |
| 123 | TBD | TBD | TBD | TBD |
| Point 3 | TBD | TBD | TBD | TBD |
| ND | TBD | TBD | TBD | TBD |
| Flag | TBD | TBD | TBD | TBD |
| Hook | TBD | TBD | TBD | TBD |
| Rally | TBD | TBD | TBD | TBD |
| 86% context | TBD | TBD | TBD | TBD |
| Parent/child mapping | TBD | TBD | TBD | TBD |

## Schema Validation
| Check | M15 | M5 | M1 | Status |
|---|---|---|---|---|
| Required fields present | TBD | TBD | TBD | PENDING |
| Allowed label_type values | TBD | TBD | TBD | PENDING |
| Direction values valid | TBD | TBD | TBD | PENDING |
| Confidence values valid | TBD | TBD | TBD | PENDING |
| Source validation status present | TBD | TBD | TBD | PENDING |
| No GENERIC_86 context | TBD | TBD | TBD | PENDING |

## Source Alignment Review
Questions:
1. Are Z labels justified by NDS structure?
2. Are N/S labels sequence-aware?
3. Is N3 separated from S3?
4. Is 123 context classified?
5. Is ND treated as Near Death?
6. Is ND not limited to flag endings?
7. Is 86% context-specific?
8. Are Hook A and B separated if labeled?
9. Is Rally treated as Trend?
10. Are uncertain rules marked SOURCE_VALIDATION_REQUIRED?

## Sequence Review
| Sequence element | Present? | Timestamp | Valid order? | Notes |
|---|---|---|---|---|
| Z | TBD | TBD | TBD | TBD |
| N1 | TBD | TBD | TBD | TBD |
| S1 | TBD | TBD | TBD | TBD |
| N2 | TBD | TBD | TBD | TBD |
| S2 | TBD | TBD | TBD | TBD |
| N3 | TBD | TBD | TBD | TBD |
| S3 | TBD | TBD | TBD | TBD |

## Point 3 Review
| point3_label_id | timeframe | status | related_123 | related_ND | related_Flag | Notes |
|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## ND Review
| ND label | timeframe | direction | terminal extreme | prior extreme broken? | 86 context | confirmed? | Notes |
|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 86% Review
| label_id | timeframe | context | reference_start | reference_end | ideal_level | actual_level | deviation | Notes |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Multi-Timeframe Review
| Parent label | Parent TF | Child labels | Child TF | Alignment status | Notes |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## Confidence Distribution
| Confidence | Count | Usable for detector validation? |
|---|---:|---|
| CONFIRMED | TBD | Yes |
| PROBABLE | TBD | Maybe |
| UNCERTAIN | TBD | No |
| REQUIRES_REVIEW | TBD | No |

## Final Decision
Allowed final statuses:
- PASS
- PASS_WITH_WARNINGS
- NEEDS_REVISION
- FAIL

| Area | Status | Notes |
|---|---|---|
| Schema validity | PENDING | TBD |
| Source alignment | PENDING | TBD |
| Sequence validity | PENDING | TBD |
| Point 3 logic | PENDING | TBD |
| ND labels | PENDING | TBD |
| 86% labels | PENDING | TBD |
| Multi-timeframe mapping | PENDING | TBD |
| Detector readiness | PENDING | TBD |

## Next Step
If PASS or PASS_WITH_WARNINGS: start sequence state-machine tests and core model skeleton. Otherwise, revise labels first.
