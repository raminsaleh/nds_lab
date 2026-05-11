# NDS Source Alignment v1

## Purpose

This document aligns repository modeling, algorithm design, and future code implementation with the NDS source materials. It prevents interpretation drift. Every mathematical model, detection rule, AI layer, risk-management rule, and implementation detail must remain subordinate to original NDS source logic.

## 1. Source Priority Rule

All repository specifications, algorithms, tests, and implementation decisions must follow the original NDS source material. If there is conflict between general technical interpretation, conventional market-structure analysis, machine-learning convenience, coding simplification, or operational interpretation and NDS source material, the source material takes priority.

## 2. Source Confidence Levels

- `SOURCE_CONFIRMED`: explicitly present in source material.
- `SOURCE_COMPATIBLE_INTERPRETATION`: not written as one exact sentence, but consistent with multiple source sections and not contradictory.
- `SOURCE_VALIDATION_REQUIRED`: operationally useful or inferred from visuals/user explanation/partial source context, but requiring validation.

## 3. Core NDS Geometry

NDS is a market-geometry framework, not a simple swing-high/swing-low model. Core geometry includes nodes, cycles, trend functions, pullback functions, flags, hooks, rally/trend structures, 123 structures, ND / Near Death, symmetry, fractal timeframe relationships, 86% reference zones, AI feedback refinement, and GARCH-based risk management.

## 4. Canonical NDS Sequence

Canonical sequence:

```text
Z -> N1 -> S1 -> N2 -> S2 -> N3 -> S3
```

Transition rules:

```text
f(Z) = N1
f(N_i) = S_i
f(S_i) = N_{i+1}
```

N3 and S3 must not be treated as equivalent. N3 completes the three-leg trend-side movement. S3 completes the full cycle and may start the next cycle.

## 5. 123 Structures

The term 123 appears in multiple contexts: hook closure, fractal leg construction, rally geometry, flag termination/reversal, and point 3 decision logic. It must not be reduced to a generic retail chart pattern.

## 6. ND / Near Death

ND stands for Near Death. It is a fractal reversal structure near the terminal area of any movement, not only flags. Typical ND: terminal extreme, initial reversal, return toward prior extreme, failure to break that extreme, rejection near a reference zone often around 86%, and continuation of reversal.

## 7. Flag Model

Flag formation is a geometric/polynomial market structure involved in node formation, continuation, reversal preparation, hook geometry, and cycle progression. Observed components include SMI/BMI, Z, LVS, and F. Exact formal definitions require validation.

## 8. Hook Geometry

NDS sources identify Hook Type A and Hook Type B in positive and negative cycles. Hook validation requires Y-axis price geometry, X-axis time/sequence geometry, symmetry, 123 context, flag context, ND context, and 86% context.

## 9. Rally Geometry

In NDS, Rally = Trend. A rally may be represented as a 123 structure and may consist of three symmetric segments. Point 3 is a decision area: rejection -> ND, break -> Flag continuation.

## 10. 86% Reference System

The 86% level appears in multiple contexts and must not be treated as one universal hard-coded formula. Contexts include hook closure, cycle closure, Point Z, ND near-retest, target projection, flag-hook visual examples, and rally retracement/accrued movement closure.

## 11. Fractal Multi-Timeframe Logic

Common source rule: one higher-timeframe movement approximately corresponds to three lower-timeframe movements. Practical initial hierarchy: M15 -> M5 -> M1. Higher timeframes provide top-down pressure; lower timeframes provide bottom-up construction.

## 12. AI and Feedback Refinement

AI refines NDS-defined structures; it does not replace NDS logic. Valid architecture: source rules -> structure detection -> function fitting -> residual calculation -> AI correction -> validation. Invalid architecture: raw OHLC -> AI -> direct buy/sell.

## 13. GARCH Money Management

GARCH is the primary risk-management method. ATR is secondary fallback/benchmark. P_rev and P_entry must remain separate. Position reduction begins only after midpoint crossing.

## 14. Visual Examples

Visual examples are source material but require manual validation. OCR or parsed text alone is insufficient for extracting final code rules.

## 15. Open Questions

- Exact target projection formula.
- Exact 86% reference move per context.
- Full Hook A vs Hook B definitions.
- Formal SMI/BMI/LVS definitions.
- Calibration of pressure and node displacement coefficients.
- Tolerance bands for 86%, symmetry, and point 3 rejection.
