import pandas as pd

from backtesting.feature_engine import compute_features

from backtesting.mtf_engine import (
    find_child_candles,
    find_lower_tf_fvgs,
    select_latest_fvg,
    build_fvg_object
)

print("\n" + "=" * 80)
print("UNICORN MTF DISCOVERY")
print("=" * 80)

# ============================================================
# LOAD DATA
# ============================================================

df_1m = pd.read_csv("data/raw/nifty_1m_master.csv")
df_5m = pd.read_csv("data/processed/nifty_5m_master.csv")

for df in [df_1m, df_5m]:

    df["datetime"] = pd.to_datetime(df["datetime"])

    df.set_index("datetime", inplace=True)

    df.rename(columns={
        "open":"Open",
        "high":"High",
        "low":"Low",
        "close":"Close",
        "volume":"Volume"
    }, inplace=True)

print("\nComputing Features...")

df_1m = compute_features(df_1m)
df_5m = compute_features(df_5m)

# ============================================================
# FIND VALID 5M CONTEXTS
# ============================================================

contexts = []

for i in range(len(df_5m)-20):

    if not df_5m["SWEEP_SWING_LOW"].iloc[i]:
        continue

    # ---------------- MSS ----------------

    mss_window = df_5m["BOS_BULLISH"].iloc[i:i+6]

    if not mss_window.any():
        continue

    mss_idx = mss_window[mss_window].index[0]

    mss_pos = df_5m.index.get_loc(mss_idx)

    # ---------------- Quality FVG ----------------

    fvg_window = df_5m["QUALITY_BULLISH_FVG"].iloc[mss_pos:mss_pos+6]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window[fvg_window].index[0]

    contexts.append(
        (
            df_5m.index[i],
            mss_idx,
            fvg_idx
        )
    )

print()
print("="*80)
print("VALID 5M CONTEXTS")
print("="*80)
print("Count:", len(contexts))

# ============================================================
# DISCOVER 1M EXECUTION FVG
# ============================================================

results = []

for sweep_time, mss_time, fvg_time in contexts:

    candles = find_child_candles(
        df_1m,
        fvg_time,
        minutes=5
    )

    lower_fvgs = find_lower_tf_fvgs(
        candles,
        bullish=True,
        quality_only=True
    )

    if len(lower_fvgs) == 0:
        continue

    latest = select_latest_fvg(
        lower_fvgs
    )

    fvg = build_fvg_object(
        latest,
        bullish=True
    )

    results.append({

        "Sweep": sweep_time,

        "MSS": mss_time,

        "5M_FVG": fvg_time,

        "1M_FVG": latest.name,

        "GapATR": round(
            fvg["gap_atr"],
            3
        ),

        "Gap": round(
            fvg["gap"],
            2
        ),

        "Top": round(
            fvg["top"],
            2
        ),

        "Bottom": round(
            fvg["bottom"],
            2
        )

    })

# ============================================================
# REPORT
# ============================================================

report = pd.DataFrame(results)

print()
print("="*80)
print("DISCOVERED EXECUTION FVGs")
print("="*80)

print(report.head(20))

print()
print("="*80)
print("SUMMARY")
print("="*80)

print("5M Contexts:", len(contexts))
print("1M Execution FVGs:", len(report))

if len(report):

    print()

    print("Average GapATR:",
          round(report["GapATR"].mean(),3))

    print("Median GapATR:",
          round(report["GapATR"].median(),3))

    print("Average Gap:",
          round(report["Gap"].mean(),2))

    print()

    print("Top 10 Strongest 1M FVGs")

    print(
        report
        .sort_values(
            "GapATR",
            ascending=False
        )
        .head(10)
    )