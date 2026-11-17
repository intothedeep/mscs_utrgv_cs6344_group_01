import sys, json
import pandas as pd
d = pd.read_parquet(sys.argv[1], columns=["scope", "pnl_gross", "pnl_net", "fees", "volume_usdc"])
out = {}
for s, g in d.groupby("scope"):
    x = g.pnl_gross.sort_values(ascending=False).to_numpy()
    n = len(x); won = x[x > 0].sum()
    r = {"n": n, "win": int((x > 0).sum()), "lose": int((x < 0).sum()),
         "won_M": won / 1e6, "lost_M": -x[x < 0].sum() / 1e6, "fees_M": g.fees.sum() / 1e6,
         "vol_B": g.volume_usdc.sum() / 1e9, "med_gross": float(pd.Series(x).median()),
         "net_win": int((g.pnl_net > 0).sum())}
    for k in (0.01, 0.03, 0.10):
        top = x[: int(n * k)]
        r[f"top{int(k*100)}_share_won"] = top[top > 0].sum() / won
    out[s] = r
print(json.dumps(out, indent=1))
