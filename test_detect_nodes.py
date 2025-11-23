import pandas as pd
from src.python.nds.detect_nodes import detect_nodes, NDSParams

def test_smoke():
    times = pd.date_range("2025-01-01", periods=30, freq="T")
    prices = [100,101,102,103,102,101,100, 99,100,101,102,103,104,103,102,101, 102,103,104,103,102,101,100,99, 100,101,102,101,100,99]
    df = pd.DataFrame({"time":times, "open":prices, "high":[p+0.5 for p in prices], "low":[p-0.5 for p in prices], "close":prices})
    nodes = detect_nodes(df, NDSParams())
    assert isinstance(nodes, pd.DataFrame)
    assert set(["bar_index","time","price","node_type"]).issubset(nodes.columns)
