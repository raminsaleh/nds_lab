# NDS Data Quality Report v1

## Purpose
Define data-quality checks required before NDS labeling, detector development, GARCH modeling, or backtesting.

## Target Instrument
- US30 / Dow Jones
- Required timeframes: M15, M5, M1

## Required Checks
1. Required columns exist.
2. Timestamps parse correctly.
3. Timestamps are sorted ascending.
4. Timestamps are unique.
5. Duplicate timestamps are resolved.
6. Missing candles / gaps are documented.
7. OHLC integrity is valid.
8. Outliers are flagged, not automatically deleted.
9. Volume/spread availability is documented.
10. Broker/source consistency is documented.

## Required Columns Table
| Timeframe | timestamp | open | high | low | close | volume | spread | Status |
|---|---|---|---|---|---|---|---|---|
| M1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | PENDING |
| M5 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | PENDING |
| M15 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | PENDING |

## OHLC Integrity Rule
Every candle must satisfy:
```text
high >= open
high >= close
low <= open
low <= close
high >= low
```

## Missing Candle Check
Expected intervals:
- M1: 1 minute
- M5: 5 minutes
- M15: 15 minutes

Do not fill missing candles unless the fill method is explicitly documented.

## Outlier Rule
Do not delete outliers automatically. Outliers may be relevant for LVS, spike behavior, Point Z, ND terminal extremes, and GARCH volatility response.

## Final Quality Summary
| Timeframe | Quality status | Main issues | Usable for labeling? | Usable for detector development? |
|---|---|---|---|---|
| M1 | PENDING | TBD | TBD | TBD |
| M5 | PENDING | TBD | TBD | TBD |
| M15 | PENDING | TBD | TBD | TBD |

## No-Go Conditions
Do not proceed if timestamps cannot be parsed, OHLC values are invalid, duplicate timestamps remain unresolved, major gaps are undocumented, M1/M5/M15 coverage does not overlap, source is unknown, or status is FAIL.
