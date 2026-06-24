import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN LOOKAHEAD AUDIT")
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
# COMPONENTS
# ============================================================

sweep = data["SWEEP_SWING_LOW"]
mss = data["BOS_BULLISH"]
quality_fvg = data["QUALITY_BULLISH_FVG"]

# ============================================================
# AUDIT
# ============================================================

audit_rows = []

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    sweep_time = data.index[i]

    # MSS within next 5 candles

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window.idxmax()

    mss_pos = data.index.get_loc(
        mss_idx
    )

    mss_time = data.index[
        mss_pos
    ]

    # FVG within next 5 candles

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window.idxmax()

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    fvg_time = data.index[
        fvg_pos
    ]

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    # RETEST

    for j in range(
        fvg_pos + 1,
        min(
            fvg_pos + 11,
            len(data)
        )
    ):

        candle_low = data[
            "Low"
        ].iloc[j]

        candle_close = data[
            "Close"
        ].iloc[j]

        candle_open = data[
            "Open"
        ].iloc[j]

        inside_zone = (

            candle_low <= fvg_top

            and

            candle_low >= fvg_bottom

        )

        bullish_close = (
            candle_close > candle_open
        )

        if (
            inside_zone
            and
            bullish_close
        ):

            entry_time = data.index[j]

            audit_rows.append({

                "Sweep":
                    sweep_time,

                "MSS":
                    mss_time,

                "FVG":
                    fvg_time,

                "Entry":
                    entry_time,

                "Sweep_to_MSS":
                    (
                        mss_time
                        -
                        sweep_time
                    ),

                "MSS_to_FVG":
                    (
                        fvg_time
                        -
                        mss_time
                    ),

                "FVG_to_Entry":
                    (
                        entry_time
                        -
                        fvg_time
                    )

            })

            break

# ============================================================
# REPORT
# ============================================================

audit_df = pd.DataFrame(
    audit_rows
)

print()

print(
    "Total Entries:",
    len(audit_df)
)

print()

print(
    audit_df.head(20)
)

print()

if len(audit_df):

    print("=" * 80)
    print("TIMING ANALYSIS")
    print("=" * 80)

    print(
        "Average Sweep->MSS:",
        audit_df[
            "Sweep_to_MSS"
        ].mean()
    )

    print(
        "Average MSS->FVG:",
        audit_df[
            "MSS_to_FVG"
        ].mean()
    )

    print(
        "Average FVG->Entry:",
        audit_df[
            "FVG_to_Entry"
        ].mean()
    )

    audit_df["BAD_ENTRY"] = (
        audit_df["Entry"]
        <=
        audit_df["FVG"]
    )

    audit_df["BAD_FVG"] = (
        audit_df["FVG"]
        <
        audit_df["MSS"]
    )

    audit_df["BAD_MSS"] = (
        audit_df["MSS"]
        <
        audit_df["Sweep"]
    )

    bad_rows = audit_df[

        audit_df["BAD_ENTRY"]

        |

        audit_df["BAD_FVG"]

        |

        audit_df["BAD_MSS"]

    ]

    print("\nBAD ROWS")
    print("=" * 80)

    print(
        bad_rows[
            [
                "Sweep",
                "MSS",
                "FVG",
                "Entry",
                "BAD_ENTRY",
                "BAD_FVG",
                "BAD_MSS"
            ]
        ]
    )

    # print()

    # print(
    #     "Invalid Sequences:",
    #     int(
    #         invalid.sum()
    #     )
    # )