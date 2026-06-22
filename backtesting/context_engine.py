import pandas as pd


def build_context(data):

    bullish_context = (

        (data["EMA20"] > data["EMA50"])

        &

        data["BULLISH_STRUCTURE"]

    )

    bearish_context = (

        (data["EMA20"] < data["EMA50"])

        &

        data["BEARISH_STRUCTURE"]

    )

    range_context = (

        ~bullish_context

        &

        ~bearish_context

    )

    return pd.DataFrame({

        "BULLISH_CONTEXT": bullish_context,

        "BEARISH_CONTEXT": bearish_context,

        "RANGE_CONTEXT": range_context

    })