import pandas as pd

def add_smc_features(data):

    data = data.copy()

    # ==========================
    # BULLISH FVG
    # ==========================
    data["BullishFVG"] = (
        data["Low"]
        >
        data["High"].shift(2)
    )

    # ==========================
    # BEARISH FVG
    # ==========================
    data["BearishFVG"] = (
        data["High"]
        <
        data["Low"].shift(2)
    )

    # ==========================
    # LIQUIDITY HIGH
    # ==========================
    data["LiquidityHigh"] = (
        data["High"]
        .rolling(20)
        .max()
    )

    # ==========================
    # LIQUIDITY LOW
    # ==========================
    data["LiquidityLow"] = (
        data["Low"]
        .rolling(20)
        .min()
    )

    # ==========================
    # BOS BULLISH
    # ==========================
    data["BOS_Bullish"] = (
        data["Close"]
        >
        data["High"].shift(1)
    )

    # ==========================
    # BOS BEARISH
    # ==========================
    data["BOS_Bearish"] = (
        data["Close"]
        <
        data["Low"].shift(1)
    )

    return data