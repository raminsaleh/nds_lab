# NDS GitHub Actions v1

## Purpose

This package adds the first GitHub Actions workflow for the NDS project.

The workflow runs the current Python test suite automatically on:

- push to `main`
- pull request to `main`
- manual workflow dispatch

## Added file

```text
.github/workflows/python-tests.yml
```

## What it runs

```bash
python -m pytest -q
```

## Current expected test scope

The workflow is intended to validate the first code skeleton:

- `nds_core/enums.py`
- `nds_core/models.py`
- `nds_core/label_schema.py`
- `nds_core/label_validation.py`
- `nds_core/sequence_state.py`
- `nds_core/sequence_engine.py`
- `tests/test_label_schema.py`
- `tests/test_sequence_state.py`

## What this does not do

This workflow does not run:

- detector backtests
- GARCH estimation
- MT5 export
- AI model training
- market-data validation

Those should be added later as separate workflows after the related code exists.

## Upload instruction

Upload the `.github` folder from this package to the root of the GitHub repository.

Expected final path:

```text
.github/workflows/python-tests.yml
```

Do not upload it as:

```text
.github/.github/workflows/python-tests.yml
```
