# NDS Money Management with GARCH v1

## Purpose

GARCH is the primary risk-management method. ATR is fallback/benchmark.

## Core Rules

P_rev and P_entry are separate. Target should be structurally anchored to P_rev/source-defined move. Position size = Risk / StopDistance. Do not reduce position before midpoint; after midpoint, dynamic reduction may begin.

## Required Data Fields / Implementation Notes

- `source_validation_status` must be stored for uncertain rules.
- Direction must be normalized for bullish and bearish cases.
- Multi-timeframe context must be checked for local triggers.
- 86% references must be context-specific, not generic.
- No structural component should create an automatic trade without sequence, timeframe, and risk validation.

## Invalid Uses

- Do not simplify this concept into a generic retail chart pattern.
- Do not hard-code source-validation-required interpretations.
- Do not let AI override source-defined NDS logic.
- Do not treat a local lower-timeframe event as valid without parent timeframe context.

## Open Questions

- Exact tolerance bands must be validated against NDS sources and real US30 data.
- Visual templates must be manually extracted and cross-checked.
- Formal definitions of ambiguous terms must be updated when source evidence is available.


## Status

This document is source-aligned but not final implementation code. Rules marked as validation-required must be checked against original NDS sources, visual examples, and real US30 data before being hard-coded.
