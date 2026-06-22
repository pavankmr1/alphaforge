import pandas as pd


def build_bullish_setup(
    context,
    sweep,
    rejection,
    confirmation
):

    setup = pd.Series(
        False,
        index=context.index
    )

    state = 0

    for i in range(len(context)):

        # Start setup only when context exists
        if state == 0:

            if context.iloc[i] and sweep.iloc[i]:
                state = 1

        # Wait for rejection
        elif state == 1:

            if rejection.iloc[i]:
                state = 2

        # Wait for confirmation
        elif state == 2:

            if confirmation.iloc[i]:

                setup.iloc[i] = True

                state = 0

    return setup