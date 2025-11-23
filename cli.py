from __future__ import annotations
import argparse, yaml
from pathlib import Path
from .io import read_ohlc_csv
from .detect_nodes import detect_nodes, NDSParams

def load_params(yaml_path: str) -> NDSParams:
    data = yaml.safe_load(Path(yaml_path).read_text(encoding="utf-8"))
    p = NDSParams(
        smoothing_kind=data.get("smoothing",{}).get("kind","ema"),
        smoothing_window=int(data.get("smoothing",{}).get("window",9)),
        deadzone_mode=data.get("derivative",{}).get("deadzone_mode","sigma"),
        deadzone_k=float(data.get("derivative",{}).get("deadzone_k",0.15)),
        sigma_window=int(data.get("derivative",{}).get("sigma_window",20)),
        atr_window=int(data.get("prominence",{}).get("atr_window",14)),
        prom_mode=data.get("prominence",{}).get("mode","atr"),
        k_sigma=float(data.get("prominence",{}).get("k_sigma",1.0)),
        k_atr=float(data.get("prominence",{}).get("k_atr",1.0)),
        epsilon_floor=float(data.get("prominence",{}).get("epsilon_floor",1.0)),
        tau_min_bars=int(data.get("separation",{}).get("tau_min_bars",3)),
        eps_min_atr14=float(data.get("separation",{}).get("eps_min_atr14",0.2)),
        alpha_low=float(data.get("hooks",{}).get("alpha_low",0.8)),
        alpha_high=float(data.get("hooks",{}).get("alpha_high",1.2)),
        beta_low=float(data.get("hooks",{}).get("beta_low",0.8)),
        beta_high=float(data.get("hooks",{}).get("beta_high",1.2)),
        epsilon_hook=float(data.get("hooks",{}).get("epsilon_hook",0.05)),
        w_bars=int(data.get("confirm",{}).get("w_bars",2)),
    )
    return p

def main(argv=None):
    parser = argparse.ArgumentParser(description="NDS node detection (scaffold v0.1)")
    parser.add_argument("--csv", required=True, help="Path to OHLC CSV with columns: time,open,high,low,close")
    parser.add_argument("--params", required=True, help="Path to params YAML (e.g., config/params_default.yaml)")
    parser.add_argument("--out", required=True, help="Output CSV path")
    args = parser.parse_args(argv)

    df = read_ohlc_csv(args.csv)
    p = load_params(args.params)
    nodes = detect_nodes(df, p)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    nodes.to_csv(args.out, index=False)
    print(f"✅ Nodes written: {args.out}  (count={len(nodes)})")

if __name__ == "__main__":
    main()
