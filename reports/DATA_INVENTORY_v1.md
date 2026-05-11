# NDS Data Inventory v1

## Purpose
Inventory all market data available for the NDS project before detector development.

## Primary Market
- Instrument: US30 / Dow Jones
- Initial hierarchy: M15 → M5 → M1

## Required Files
| Timeframe | Expected processed file | Status |
|---|---|---|
| M1 | `data/processed/US30_M1_clean.csv` | PENDING |
| M5 | `data/processed/US30_M5_clean.csv` | PENDING |
| M15 | `data/processed/US30_M15_clean.csv` | PENDING |

## Required Columns
Minimum:
- timestamp
- open
- high
- low
- close

Recommended:
- tick_volume
- real_volume
- spread
- broker
- symbol
- timeframe

## Dataset Registry
| dataset_id | symbol | source | timeframe | file_path | start_time | end_time | rows | status | notes |
|---|---|---|---|---|---|---|---:|---|---|
| US30_M1_001 | US30 | TBD | M1 | data/processed/US30_M1_clean.csv | TBD | TBD | TBD | PENDING | Required |
| US30_M5_001 | US30 | TBD | M5 | data/processed/US30_M5_clean.csv | TBD | TBD | TBD | PENDING | Required |
| US30_M15_001 | US30 | TBD | M15 | data/processed/US30_M15_clean.csv | TBD | TBD | TBD | PENDING | Required |

## Minimum Data Window
At least 6 months is preferred for M15/M5/M1 modeling.

## No-Go Conditions
Do not proceed to detector coding if M1/M5/M15 are missing, timestamps are inconsistent, OHLC columns are malformed, duplicates are unresolved, gaps are undocumented, or the broker/source is unknown.

## Next Step
Generate `DATA_QUALITY_REPORT_v1.md` and `TIMEFRAME_ALIGNMENT_REPORT_v1.md`.
