import pandas as pd


def compute_features(data):

    data = data.copy()

    # ==========================================
    # EMAs
    # ==========================================
    data["EMA5"] = (
        data["Close"]
        .ewm(span=5, adjust=False)
        .mean()
    )

    data["EMA9"] = (
        data["Close"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    data["EMA10"] = (
        data["Close"]
        .ewm(span=10, adjust=False)
        .mean()
    )

    data["EMA15"] = (
        data["Close"]
        .ewm(span=15, adjust=False)
        .mean()
    )

    data["EMA20"] = (
        data["Close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    data["EMA21"] = (
        data["Close"]
        .ewm(span=21, adjust=False)
        .mean()
    )

    data["EMA50"] = (
        data["Close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    data["EMA200"] = (
        data["Close"]
        .ewm(span=200, adjust=False)
        .mean()
    )

    # ==========================================
    # SMA
    # ==========================================
    data["SMA18"] = (
        data["Close"]
        .rolling(18)
        .mean()
    )

    data["SMA20"] = (
        data["Close"]
        .rolling(20)
        .mean()
    )

    data["SMA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )

    # ==========================================
    # VWAP
    # ==========================================
    data["VWAP"] = (
        (
            data["Close"]
            * data["Volume"]
        ).cumsum()
        /
        data["Volume"].cumsum()
    )

    # ==========================================
    # ATR14
    # ==========================================
    high_low = (
        data["High"]
        - data["Low"]
    )

    high_close = (
        data["High"]
        - data["Close"].shift()
    ).abs()

    low_close = (
        data["Low"]
        - data["Close"].shift()
    ).abs()

    tr = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)

    data["ATR14"] = (
        tr.rolling(14)
        .mean()
    )

    # ==========================================
    # RSI14
    # ==========================================
    delta = (
        data["Close"]
        .diff()
    )

    gain = (
        delta.where(
            delta > 0,
            0
        )
        .rolling(14)
        .mean()
    )

    loss = (
        -delta.where(
            delta < 0,
            0
        )
        .rolling(14)
        .mean()
    )

    rs = gain / loss

    data["RSI14"] = (
        100
        -
        (
            100
            /
            (1 + rs)
        )
    )

    # ==========================================
    # VOLUME
    # ==========================================
    data["VOL_MA20"] = (
        data["Volume"]
        .rolling(20)
        .mean()
    )

    data["AverageVolume"] = (
        data["Volume"]
        .rolling(20)
        .mean()
    )

    # ==========================================
    # PREVIOUS DAY LEVELS
    # ==========================================
    data["PreviousDayHigh"] = (
        data["High"]
        .shift(1)
    )

    data["PreviousDayLow"] = (
        data["Low"]
        .shift(1)
    )

    data["PreviousClose"] = (
        data["Close"]
        .shift(1)
    )

    # ==========================================
    # PIVOT
    # ==========================================
    data["Pivot"] = (
        data["PreviousDayHigh"]
        +
        data["PreviousDayLow"]
        +
        data["PreviousClose"]
    ) / 3

    # ==========================================
    # SIMPLE PRICE ALIASES
    # ==========================================
    data["Price"] = data["Close"]
    data["Market"] = data["Close"]
    data["Trend"] = data["Close"]
    data["PreviousHigh"] = data["High"].shift(1)

    data["PreviousLow"] = data["Low"].shift(1)
    from backtesting.support_resistance import (
        add_support_resistance
    )

    data = add_support_resistance(
        data
    )
    return data