import pandas as pd


def bullish_trigger(
    qualified_setup,
    bos
):

    trigger = (

        qualified_setup

        &

        bos

    )

    return trigger.fillna(False)