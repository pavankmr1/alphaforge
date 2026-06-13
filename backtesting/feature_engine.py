import pandas as pd
import numpy as np

def compute_features(data):

    df = data.copy()

    # ==========================
    # EMA
    # ==========================
    df["EMA9"] = (
        df["Close"]
        .ewm(span=9)
        .mean()
    )

    df["EMA20"] = (
        df["Close"]
        .ewm(span=20)
        .mean()
    )

    df["EMA50"] = (
        df["Close"]
        .ewm(span=50)
        .mean()
    )

    df["EMA200"] = (
        df["Close"]
        .ewm(span=200)
        .mean()
    )

    # ==========================
    # VWAP
    # ==========================
    typical_price = (
        df["High"] +
        df["Low"] +
        df["Close"]
    ) / 3

    df["VWAP"] = (
        (typical_price * df["Volume"]).cumsum()
        /
        df["Volume"].cumsum()
    )

    # ==========================
    # ATR
    # ==========================
    high_low = (
        df["High"] -
        df["Low"]
    )

    high_close = np.abs(
        df["High"] -
        df["Close"].shift()
    )

    low_close = np.abs(
        df["Low"] -
        df["Close"].shift()
    )

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)

    df["ATR14"] = (
        true_range
        .rolling(14)
        .mean()
    )

    # ==========================
    # RSI
    # ==========================
    delta = (
        df["Close"]
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

    df["RSI14"] = (
        100 -
        (
            100 /
            (1 + rs)
        )
    )

    # ==========================
    # VOLUME MA
    # ==========================
    df["VOL_MA20"] = (
        df["Volume"]
        .rolling(20)
        .mean()
    )

    return df