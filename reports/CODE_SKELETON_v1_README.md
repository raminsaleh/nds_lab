# NDS Code Skeleton v1

## Purpose

This package adds the first controlled code skeleton for the NDS project.

It includes only foundational modules:

- enums
- data models
- label schema constants
- label validation
- sequence state
- sequence engine
- initial tests

It does not include final detectors, trading signals, GARCH risk execution, AI, or MT5 execution.

## Files

```text
nds_core/
  __init__.py
  enums.py
  models.py
  label_schema.py
  label_validation.py
  sequence_state.py
  sequence_engine.py

tests/
  test_label_schema.py
  test_sequence_state.py
```

## What this validates

- label rows must follow `spec/NDS_LABEL_SCHEMA_v1.md`
- `GENERIC_86` is rejected
- invalid directions are rejected
- generic swing labels are rejected if not part of allowed NDS label types
- sequence order must be: Z → N1 → S1 → N2 → S2 → N3 → S3
- cycle is not complete at N3
- cycle completes only at S3

## What this does not do

This package does not:

- detect nodes from OHLC
- detect ND
- detect Flag
- detect Hook
- detect Rally
- compute GARCH
- generate buy/sell signals
- export MT5 orders
