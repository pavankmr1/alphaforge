import pandas as pd


def build_5m_setup(
    data_5m,
    context_5m
):

   recent_sweep = (

        data_5m["SWEEP_SWING_LOW"]

        .rolling(5)

        .max()

        .fillna(False)

        .astype(bool)

    )

   setup = (

        context_5m["BULLISH_CONTEXT"]

        &

        recent_sweep

        &

        data_5m["BOS_BULLISH"]

    )

   return setup