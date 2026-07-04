import pandas as pd

# from data.loader import load_data
from backtesting.feature_engine import (
    compute_features
)
from backtesting.strategies.unicorn import UnicornStrategy

print("=" * 80)
print("UNICORN ENGINE VALIDATION")
print("=" * 80)

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

print("\nLoading data...")

df_5m = pd.read_csv("/Users/pavan/Downloads/alphaforge/data/processed/nifty_5m_master.csv")

df_1m = pd.read_csv("/Users/pavan/Downloads/alphaforge/data/raw/nifty_1m_master.csv")

df_5m["datetime"] = pd.to_datetime(df_5m["datetime"])
df_1m["datetime"] = pd.to_datetime(df_1m["datetime"])

df_5m.set_index("datetime", inplace=True)
df_1m.set_index("datetime", inplace=True)

rename = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume"
}

df_5m.rename(columns=rename, inplace=True)
df_1m.rename(columns=rename, inplace=True)
# ----------------------------------------------------------
# FEATURES
# ----------------------------------------------------------



print("Computing Features...")

df_5m = compute_features(df_5m)
df_1m = compute_features(df_1m)
# ----------------------------------------------------------
# STRATEGY
# ----------------------------------------------------------

strategy = UnicornStrategy()

trade_no = 1

# ----------------------------------------------------------
# PROCESS EACH 5M CANDLE
# ----------------------------------------------------------

for ts5, candle5 in df_5m.iterrows():

    # ---------------------------------------
    # Set current day's high
    # ---------------------------------------

    day = ts5.date()

    strategy.set_day_high(

        df_5m[
            df_5m.index.date == day
        ]["High"].max()

    )

    # ---------------------------------------
    # Update HTF
    # ---------------------------------------

    strategy.update_5m(candle5)

    # ---------------------------------------
    # Feed corresponding 1m candles
    # ---------------------------------------

    start = ts5

    end = ts5 + pd.Timedelta(minutes=5)

    candles_1m = df_1m.loc[start:end]

    before = len(strategy.get_signals())

    for ts1, candle1 in candles_1m.iterrows():

        strategy.update_1m(candle1)

    after = len(strategy.get_signals())

    # ---------------------------------------
    # New Signal?
    # ---------------------------------------

    if after > before:

        signal = strategy.get_signals()[-1]

        print()

        print("=" * 80)
        print(f"TRADE #{trade_no}")
        print("=" * 80)

        print()

        print("STATE")
        print(strategy.state())

        print()

        print("Sweep")
        print(strategy.context.latest_sweep)

        print()

        print("MSS")
        print(strategy.context.latest_mss)

        print()

        if hasattr(strategy.context, "htf_fvg"):

            htf = strategy.context.htf_fvg

            if htf:

                print("HTF FVG")
                print(
                    f"Top={htf.top:.2f} "
                    f"Bottom={htf.bottom:.2f}"
                )

                print()

        if hasattr(strategy.context, "execution_fvg"):

            fvg = strategy.context.execution_fvg

            if fvg:

                print("Execution FVG")

                print(
                    f"Top={fvg.top:.2f}"
                )

                print(
                    f"Bottom={fvg.bottom:.2f}"
                )

                print(
                    f"Gap={fvg.gap:.2f}"
                )

                print(
                    f"ATR Ratio={fvg.gap_atr:.2f}"
                )

                print()

        print("ENTRY")

        print(signal.entry_time)

        print(signal.entry_price)

        print()

        print("STOP")

        print(signal.stop_loss)

        print()

        print("TARGET")

        print(signal.target)

        print()

        print("PASS")

        trade_no += 1

print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print()

print("Signals :", len(strategy.get_signals()))

print("State :", strategy.state())

print("Active FVGs :", len(strategy.context.active_fvgs))

valid = len(
    [
        f
        for f in strategy.context.active_fvgs
        if f.valid
    ]
)

broken = len(
    [
        f
        for f in strategy.context.active_fvgs
        if f.broken
    ]
)

used = len(
    [
        f
        for f in strategy.context.active_fvgs
        if f.used
    ]
)

print("Valid FVG :", valid)
print("Broken FVG :", broken)
print("Used FVG :", used)