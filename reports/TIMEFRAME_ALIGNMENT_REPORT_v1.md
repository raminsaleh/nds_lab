# NDS Timeframe Alignment Report v1

## Purpose
Validate alignment between M1, M5, and M15 market data before NDS labeling, detector development, backtesting, or GARCH risk modeling.

## Target Hierarchy
M15 → M5 → M1

- M15 = primary structural timeframe
- M5 = intermediate validation timeframe
- M1 = fine-structure / execution-support timeframe

## Time Range Overlap
| Timeframe | Start time | End time | Duration | Rows |
|---|---|---|---|---:|
| M1 | TBD | TBD | TBD | TBD |
| M5 | TBD | TBD | TBD | TBD |
| M15 | TBD | TBD | TBD | TBD |

| Common overlap start | Common overlap end | Overlap duration | Status |
|---|---|---|---|
| TBD | TBD | TBD | PENDING |

## Timestamp Boundary Checks
| Timeframe | Boundary rule | Misaligned candles | Status |
|---|---|---:|---|
| M1 | every minute | TBD | PENDING |
| M5 | minute % 5 == 0 | TBD | PENDING |
| M15 | minute % 15 == 0 | TBD | PENDING |

## Aggregation Checks
M1 → M5:
- open = first M1 open
- high = max M1 high
- low = min M1 low
- close = last M1 close
- volume = sum M1 volume if available

M5 → M15:
- open = first M5 open
- high = max M5 high
- low = min M5 low
- close = last M5 close
- volume = sum M5 volume if available

M1 → M15 direct aggregation should also be checked.

## Missing Child Candles
| Parent timeframe | Child timeframe | Expected child count | Parent candles with missing children | Status |
|---|---|---:|---:|---|
| M5 | M1 | 5 | TBD | PENDING |
| M15 | M5 | 3 | TBD | PENDING |
| M15 | M1 | 15 | TBD | PENDING |

## 1:3 Fractal Interpretation
M15 → M5 is exact 1:3 by standard timeframe duration. M5 → M1 is practical execution granularity, not exact 1:3.

## No-Go Conditions
Do not proceed if M1/M5/M15 have no common overlap, boundaries are misaligned, aggregation is materially inconsistent, child gaps are undocumented, timezones differ without correction, or sources differ without documentation.
