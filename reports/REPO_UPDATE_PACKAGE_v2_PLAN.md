# NDS Repo Update Package v2 Plan

## Purpose
Define the second repository update package for the NDS project.

Package v1 added the source-aligned core specification layer. Package v2 adds the data, labeling, template-validation, detector-planning, and code-architecture planning layer.

## Package v2 Goal
Prepare the repository for controlled development.

This package does not add production detector code.

It adds:
- data inventory plan
- data quality plan
- timeframe alignment plan
- labeling guidelines
- label schema
- labeling review template
- template library
- visual template validation
- prototype detector plan
- code architecture

## Files to Add

### Reports
Add to `reports/`:
- `DATA_INVENTORY_v1.md`
- `DATA_QUALITY_REPORT_v1.md`
- `TIMEFRAME_ALIGNMENT_REPORT_v1.md`
- `LABELING_GUIDELINES_v1.md`
- `LABELING_REVIEW_v1.md`
- `VISUAL_TEMPLATE_VALIDATION_v1.md`
- `PROTOTYPE_DETECTOR_PLAN_v1.md`
- `REPO_UPDATE_PACKAGE_v2_PLAN.md`

### Specs
Add to `spec/`:
- `NDS_LABEL_SCHEMA_v1.md`
- `NDS_TEMPLATE_LIBRARY_v1.md`
- `NDS_CODE_ARCHITECTURE_v1.md`

## Recommended Commit Plan

### Commit 1 — Data Preparation Reports
Message:
```text
Add NDS data inventory and quality planning reports
```
Files:
- `reports/DATA_INVENTORY_v1.md`
- `reports/DATA_QUALITY_REPORT_v1.md`
- `reports/TIMEFRAME_ALIGNMENT_REPORT_v1.md`

### Commit 2 — Labeling Specifications
Message:
```text
Add NDS labeling guidelines and label schema
```
Files:
- `reports/LABELING_GUIDELINES_v1.md`
- `reports/LABELING_REVIEW_v1.md`
- `spec/NDS_LABEL_SCHEMA_v1.md`

### Commit 3 — Template and Detector Planning
Message:
```text
Add NDS template validation and prototype detector plan
```
Files:
- `spec/NDS_TEMPLATE_LIBRARY_v1.md`
- `reports/VISUAL_TEMPLATE_VALIDATION_v1.md`
- `reports/PROTOTYPE_DETECTOR_PLAN_v1.md`

### Commit 4 — Code Architecture Plan
Message:
```text
Add NDS code architecture and repo update v2 plan
```
Files:
- `spec/NDS_CODE_ARCHITECTURE_v1.md`
- `reports/REPO_UPDATE_PACKAGE_v2_PLAN.md`

## Upload Instructions
When uploading via GitHub web UI:

1. Open the target folder in GitHub.
2. Use `Add file -> Upload files`.
3. Upload the files inside the local folder, not the folder itself.
4. Commit with the recommended commit message.

Do not upload:
```text
reports/ as reports/reports/
spec/ as spec/spec/
```

Correct:
```text
reports/DATA_INVENTORY_v1.md
spec/NDS_LABEL_SCHEMA_v1.md
```

## Files Not to Add Yet
Do not add implementation code yet:
- `nds_core/enums.py`
- `nds_core/models.py`
- `nds_core/label_validation.py`
- `nds_core/sequence_state.py`
- `nds_core/sequence_engine.py`
- `nds_core/nd_near_death.py`
- `nds_risk/garch_volatility.py`
- `nds_ai/random_forest_residual.py`

## Exit Criteria
Package v2 is complete when:
- all listed files exist in the correct folders
- no duplicate nested folders exist
- label schema exists
- template library exists
- code architecture exists
- data reports exist
- labeling reports exist
- prototype detector plan exists

## Next Phase
After package v2 is committed, the next phase is the first code skeleton:
- `nds_core/enums.py`
- `nds_core/models.py`
- `nds_core/label_schema.py`
- `nds_core/label_validation.py`
- `nds_core/sequence_state.py`
- `nds_core/sequence_engine.py`
- tests for label schema, label validation, sequence state, and sequence engine.
