import pandas as pd


def build_mtf_context(data_15m):

    bullish = (

        data_15m["EMA20"]

        >

        data_15m["EMA50"]

    )

    bearish = (

        data_15m["EMA20"]

        <

        data_15m["EMA50"]

    )

    context = pd.DataFrame({

        "BULLISH_CONTEXT": bullish,

        "BEARISH_CONTEXT": bearish

    })

    return context