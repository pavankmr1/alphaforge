import pandas as pd


def build_bullish_setup_v2(

    session_ids,
    context,
    sweep,
    rejection,
    confirmation

):

    setup = pd.Series(
        False,
        index=context.index
    )

    current_session = None

    state = 0

    for i in range(len(context)):

        session = session_ids.iloc[i]

        # -------------------------
        # NEW SESSION RESET
        # -------------------------

        if session != current_session:

            current_session = session

            state = 0

        # -------------------------
        # STATE 0
        # WAIT FOR SWEEP
        # -------------------------

        if state == 0:

            if context.iloc[i] and sweep.iloc[i]:

                state = 1

        # -------------------------
        # STATE 1
        # WAIT FOR REJECTION
        # -------------------------

        elif state == 1:

            if rejection.iloc[i]:

                state = 2

        # -------------------------
        # STATE 2
        # WAIT FOR CONFIRMATION
        # -------------------------

        elif state == 2:

            if confirmation.iloc[i]:

                setup.iloc[i] = True

                state = 0

    return setup