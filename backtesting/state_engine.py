import pandas as pd


def sequence_signal(
    first_event,
    second_event,
    third_event=None,
    lookahead=5
):

    signal = pd.Series(
        False,
        index=first_event.index
    )

    first_idx = first_event[
        first_event
    ].index

    for ts in first_idx:

        pos = (
            first_event.index
            .get_loc(ts)
        )

        end_pos = min(
            pos + lookahead,
            len(first_event) - 1
        )

        second_window = (
            second_event.iloc[
                pos:end_pos + 1
            ]
        )

        if not second_window.any():
            continue

        second_pos = (
            second_window[
                second_window
            ]
            .index[0]
        )

        second_loc = (
            first_event.index
            .get_loc(second_pos)
        )

        # ==========================
        # TWO-STEP SEQUENCE
        # A -> B
        # ==========================
        if third_event is None:

            signal.iloc[
                second_loc
            ] = True

            continue

        # ==========================
        # THREE-STEP SEQUENCE
        # A -> B -> C
        # ==========================

        third_end = min(
            second_loc + lookahead,
            len(first_event) - 1
        )

        third_window = (
            third_event.iloc[
                second_loc:third_end + 1
            ]
        )

        if not third_window.any():
            continue

        third_pos = (
            third_window[
                third_window
            ]
            .index[0]
        )

        third_loc = (
            first_event.index
            .get_loc(
                third_pos
            )
        )

        signal.iloc[
            third_loc
        ] = True

    return signal