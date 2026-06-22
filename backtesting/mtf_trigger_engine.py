import pandas as pd


def build_1m_trigger(
    data_1m,
    setup_1m
):

    trigger = (

        setup_1m

        &

        data_1m["BOS_BULLISH"]

    )

    return trigger