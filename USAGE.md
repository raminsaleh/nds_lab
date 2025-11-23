# NDS Scaffold v0.1 — Usage

## Run from repo root
```bash
python -m src.python.nds.cli --csv data/us30_m15_sample.csv --params config/params_default.yaml --out outs/nodes_us30_m15.csv
```

## Expected CSV input
```
time,open,high,low,close
2024-01-01T00:00:00Z, ...  # etc.
```

## Outputs
CSV with columns:
```
bar_index,time,price,node_type,higher_than_prev,hook_quality,seq_label,σ_t,R̂,SL,TP,quality_score
```

## Notes
- Hook quality is placeholder (H0) here; will be implemented after sequence wiring and symmetry checks.
- Deadzone & prominence parameters are provisional; calibrate from Evidence Map and update `config/params_default.yaml`.
