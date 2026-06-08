import pandas as pd

# ==========================================
# DETECT MARKET REGIME
# ==========================================
def detect_regime(
    data
):

    close = data["Close"]

    ema20 = (
        close.ewm(span=20)
        .mean()
    )

    ema50 = (
        close.ewm(span=50)
        .mean()
    )

    atr_proxy = (
        data["High"] -
        data["Low"]
    ).rolling(14).mean()

    trend_strength = (
        abs(ema20 - ema50)
        / close
    )

    volatility_strength = (
        atr_proxy / close
    )

    regime = pd.Series(
        index=data.index,
        dtype="object"
    )

    # ======================================
    # TREND / RANGE
    # ======================================
    regime[
        trend_strength > 0.01
    ] = "TRENDING"

    regime[
        trend_strength <= 0.01
    ] = "RANGING"

    # ======================================
    # VOLATILITY
    # ======================================
    regime[
        volatility_strength > 0.02
    ] += "_HIGH_VOL"

    regime[
        volatility_strength <= 0.02
    ] += "_LOW_VOL"

    return regime