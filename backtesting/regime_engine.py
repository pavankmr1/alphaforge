import pandas as pd


def detect_trending_market(data):

    ema20 = data["EMA20"]

    ema50 = data["EMA50"]

    trend_strength = (
        (
            ema20 - ema50
        ).abs()
        /
        data["Close"]
    )

    trending = (

        (ema20 > ema50)

        &

        (
            trend_strength
            > 0.003
        )

    )

    return trending


def detect_ranging_market(data):

    ema20 = data["EMA20"]

    ema50 = data["EMA50"]

    trend_strength = (
        (
            ema20 - ema50
        ).abs()
        /
        data["Close"]
    )

    ranging = (
        trend_strength
        <= 0.003
    )

    return ranging


def build_regime(data):

    trending = (
        detect_trending_market(
            data
        )
    )

    ranging = (
        detect_ranging_market(
            data
        )
    )

    return pd.DataFrame({

        "TRENDING":
            trending,

        "RANGING":
            ranging

    })