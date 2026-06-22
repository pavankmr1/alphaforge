import pandas as pd


def broadcast_context(
    context_15m,
    data_5m
):

    broadcasted = (

        context_15m

        .reindex(
            data_5m.index,
            method="ffill"
        )

    )

    return broadcasted