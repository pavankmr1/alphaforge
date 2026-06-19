import pandas as pd


def event_followed_by(
    trigger,
    confirmation,
    lookahead=3
):

    result = pd.Series(
        False,
        index=trigger.index
    )

    trigger_idx = trigger[
        trigger
    ].index

    for ts in trigger_idx:

        pos = (
            trigger.index
            .get_loc(ts)
        )

        future_end = min(
            pos + lookahead,
            len(trigger) - 1
        )

        future_window = confirmation.iloc[
            pos : future_end + 1
        ]

        if future_window.any():

            result.iloc[pos] = True

    return result