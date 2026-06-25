import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN COST AUDIT")
print("=" * 80)

# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(
    "data/processed/nifty_15m_master.csv"
)

data["datetime"] = pd.to_datetime(
    data["datetime"]
)

data.set_index(
    "datetime",
    inplace=True
)

data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    },
    inplace=True
)

# ============================================================
# FEATURES
# ============================================================

data = compute_features(data)

# ============================================================
# BUILD UNICORN ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

sweep = data["SWEEP_SWING_LOW"]
mss = data["BOS_BULLISH"]
quality_fvg = data["QUALITY_BULLISH_FVG"]

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    mss_window = mss.iloc[i:i+6]

    if not mss_window.any():
        continue

    mss_idx = mss_window[
        mss_window
    ].index[0]

    mss_pos = data.index.get_loc(
        mss_idx
    )

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window[
        fvg_window
    ].index[0]

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    for j in range(
        fvg_pos + 1,
        min(
            fvg_pos + 11,
            len(data)
        )
    ):

        inside_zone = (

            data["Low"].iloc[j]
            <=
            fvg_top

            and

            data["Low"].iloc[j]
            >=
            fvg_bottom

        )

        bullish_close = (

            data["Close"].iloc[j]
            >
            data["Open"].iloc[j]

        )

        if (
            inside_zone
            and
            bullish_close
        ):
            entries.iloc[j] = True
            break

# ============================================================
# ORIGINAL EXIT
# ============================================================

exits = data["BOS_BEARISH"]

# ============================================================
# COST TESTS
# ============================================================

results = []

for fee in [

    0.0000,   # no cost

    0.0005,   # 0.05%

    0.0010,   # 0.10%

    0.0015,   # 0.15%

    0.0020    # 0.20%

]:

    portfolio = vbt.Portfolio.from_signals(

        close=data["Close"],

        entries=entries,

        exits=exits,

        fees=fee,

        init_cash=100000,

        freq="15m"
    )

    results.append({

        "Fee%":
            round(
                fee * 100,
                3
            ),

        "Trades":
            portfolio.trades.count(),

        "Return":
            round(
                float(
                    portfolio.total_return()
                ),
                4
            ),

        "Sharpe":
            round(
                float(
                    portfolio.sharpe_ratio()
                ),
                4
            ),

        "WinRate":
            round(
                float(
                    portfolio.trades.win_rate()
                ),
                4
            ),

        "PF":
            round(
                float(
                    portfolio.trades.profit_factor()
                ),
                4
            ),

        "MaxDD":
            round(
                float(
                    portfolio.max_drawdown()
                ),
                4
            )

    })

# ============================================================
# RESULTS
# ============================================================

results_df = pd.DataFrame(
    results
)

print()

print("=" * 80)
print("UNICORN COST AUDIT RESULTS")
print("=" * 80)

print(results_df)

print()

print("=" * 80)
print("SURVIVAL TEST")
print("=" * 80)

for _, row in results_df.iterrows():

    status = "PASS"

    if row["PF"] < 1.0:
        status = "FAIL"

    print(
        f"Fee {row['Fee%']}% | "
        f"PF={row['PF']} | "
        f"Return={row['Return']} | "
        f"{status}"
    )