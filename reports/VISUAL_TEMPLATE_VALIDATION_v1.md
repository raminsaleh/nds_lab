# NDS Visual Template Validation v1

## Purpose
Validate NDS structural templates against visual examples from NDS source materials.

## Core Principle
Visual examples are source evidence, but they must not be converted into hard-coded rules without manual validation.

## Inputs
- `spec/NDS_VISUAL_EXAMPLES_INDEX_v1.md`
- `spec/NDS_TEMPLATE_LIBRARY_v1.md`
- `spec/NDS_SOURCE_ALIGNMENT_v1.md`
- `spec/NDS_CORE_SPEC_v2.md`

## Validation Status
- VISUALLY_CONFIRMED
- VISUALLY_SUPPORTED_BUT_AMBIGUOUS
- SOURCE_COMPATIBLE_NEEDS_MORE_VISUALS
- SOURCE_VALIDATION_REQUIRED
- NOT_READY_FOR_DETECTOR

## Template Validation Table
| Template ID | Component | Visual support | Status | Notes |
|---|---|---|---|---|
| TPL_CYCLE_CANONICAL_v1 | Cycle | Persian cycle diagrams / sequencing pages | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | Exact 86% anchor needs validation |
| TPL_NODE_SEQUENCE_v1 | Node sequence | Sequencing material | VISUALLY_CONFIRMED | Sequence order is source-aligned |
| TPL_123_CONTEXTUAL_v1 | 123 | 123 Flag Hook / Rally 123 visuals | VISUALLY_CONFIRMED | Must remain context-specific |
| TPL_POINT3_DECISION_v1 | Point 3 | Point 3 / ND / F diagrams | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | Break/rejection threshold unresolved |
| TPL_ND_NEAR_DEATH_v1 | ND | 123 / terminal reversal visuals | SOURCE_COMPATIBLE_NEEDS_MORE_VISUALS | Exact source wording still needs validation |
| TPL_FLAG_CONTEXTUAL_v1 | Flag | Persian Flag pages | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | SMI/BMI/LVS definitions need validation |
| TPL_HOOK_TYPE_A_v1 | Hook A | Hook Type A diagrams | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | X/Y ratios need extraction |
| TPL_HOOK_TYPE_B_v1 | Hook B | Hook Type B diagrams | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | Difference from Hook A needs mapping |
| TPL_RALLY_TREND_v1 | Rally | Rally 123 diagrams | VISUALLY_CONFIRMED | Rally = Trend source-aligned |
| TPL_86_CONTEXTUAL_REFERENCE_v1 | 86% | 86 / 86.4 visual examples | VISUALLY_SUPPORTED_BUT_AMBIGUOUS | Context anchors must be separated |
| TPL_MULTITIMEFRAME_PARENT_CHILD_v1 | Multi-timeframe | Fractal / nested cycle sections | SOURCE_COMPATIBLE_NEEDS_MORE_VISUALS | Needs real-data validation |

## Key Validation Issues
| Issue ID | Severity | Description | Affected templates | Required action |
|---|---|---|---|---|
| VIS_001 | HIGH | Exact 86% reference anchor unclear across contexts | 86%, Hook, Cycle, ND | Manually annotate source examples |
| VIS_002 | HIGH | Hook A vs Hook B distinction not formalized | Hook A, Hook B | Extract X/Y geometry from diagrams |
| VIS_003 | MEDIUM | SMI/BMI/LVS definitions require source mapping | Flag | Review Persian Academy flag pages |
| VIS_004 | HIGH | Point 3 break/rejection threshold undefined | Point 3, ND, Flag | Validate against chart examples and labels |
| VIS_005 | MEDIUM | ND abbreviation and exact source wording require confirmation | ND | Source text / visual review |

## Detector Readiness Summary
| Component | Detector readiness | Reason |
|---|---|---|
| Node sequence | READY_FOR_STATE_MACHINE_PROTOTYPE | Sequence order is clear |
| 123 contextual classification | READY_FOR_PROTOTYPE | Context-specific rule is clear |
| Point 3 decision | NOT_READY_FOR_FINAL_DETECTOR | Thresholds unresolved |
| ND | PROTOTYPE_ONLY | Structure defined, thresholds unresolved |
| Flag | PROTOTYPE_ONLY | Components visible, definitions unresolved |
| Hook A | PROTOTYPE_ONLY | Distinct type supported, geometry unresolved |
| Hook B | PROTOTYPE_ONLY | Distinct type supported, geometry unresolved |
| Rally | READY_FOR_PROTOTYPE | Rally = Trend and 123 relation supported |
| 86% engine | PROTOTYPE_ONLY | Context separation clear, anchors unresolved |
| Multi-timeframe | READY_FOR_CONTEXT_PROTOTYPE | General hierarchy clear |

## Final Decision
Overall status:
```text
PASS_WITH_WARNINGS
```

State machine and label validation may begin. Prototype detectors may be designed. Final production detectors must wait for template-level validation.
