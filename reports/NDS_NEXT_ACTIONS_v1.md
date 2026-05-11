# NDS Next Actions v1

## Purpose

Short execution checklist for the next repository update cycle.

## Immediate Goal

Create the source-aligned specification layer. Do not start detector coding yet.

## First 10 Repository Actions

1. Create `spec/NDS_SOURCE_ALIGNMENT_v1.md`.
2. Create `spec/NDS_CORE_SPEC_v2.md`.
3. Create `spec/NDS_TERMINOLOGY_SOURCE_GLOSSARY_v1.md`.
4. Create `spec/NDS_GEOMETRY_COMPONENTS_v1.md`.
5. Create detailed structural specs: 123, ND, Flag, Hook, Rally, 86%.
6. Create timeframe and sequence specs: Multi-Timeframe, Nested Cycle, Sequence Execution.
7. Create AI and Risk specs.
8. Create Visual Examples Index.
9. Create `spec/NDS_SPEC_CHANGELOG.md`.
10. Create `reports/NDS_IMPLEMENTATION_ROADMAP_v1.md`.

## Recommended Commit Plan

### Commit 1 — Source and Core Specs

Message: `Add source-aligned NDS core specifications`

Files: source alignment, core spec, terminology glossary, geometry components, changelog, spec README.

### Commit 2 — Structural Geometry Specs

Message: `Add NDS structural geometry specifications`

Files: 123, ND, Flag, Hook, Rally, 86%.

### Commit 3 — Timeframe, AI, Risk, and Visual Specs

Message: `Add NDS timeframe, AI, risk, and visual validation specs`

Files: Multi-Timeframe, Nested Cycle, Sequence Execution, AI, GARCH, Visual Index.

### Commit 4 — Roadmap and Next Actions

Message: `Add NDS implementation roadmap and next actions`

Files: Implementation Roadmap and Next Actions.

## Files Not to Create Yet

Do not create detector code yet. Delay `nds_core/*.py`, `nds_risk/*.py`, and `nds_ai/*.py` until specs, data quality, labels, and visual template validation exist.

## First Technical Work After Specs

1. Build data inventory.
2. Validate M1/M5/M15 data quality.
3. Create label schema.
4. Manually label one sample window.
5. Build visual template library.
6. Start prototype detectors only after validation.

## No-Go Conditions

Do not proceed to detector coding if source specs are missing, terminology is unresolved, ND is ambiguous, 86% contexts are merged, Hook A/B are merged, timeframe alignment is unverified, no manual labels exist, or visual templates are not indexed.
