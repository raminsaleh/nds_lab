# NDS ND / Near Death Model v1

## Purpose

ND stands for Near Death. It is a fractal reversal structure near the terminal area of any movement, not only a flag ending.

## Core Rules

Typical ND: terminal extreme -> initial reversal -> return toward prior extreme -> failure to break prior extreme -> rejection near reference zone, often around 86% -> continuation of reversal. ND is a trigger candidate, not an automatic trade.

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
