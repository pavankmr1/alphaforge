import pandas as pd


def execute_mapping(
    logic,
    data
):

    logic_type = logic.get(
        "logic_type"
    )

    # ==========================================
    # CONFIRMATION CANDLE
    # ==========================================
    if logic_type == "confirmation":

        signal = (

            (
                data["Close"]
                -
                data["Open"]
            )

            >

            data["ATR14"] * 0.5

        )

        return signal.fillna(
            False
        )

    # ==========================================
    # REJECTION
    # ==========================================
    if logic_type == "rejection":

        body = (

            data["Close"]
            -
            data["Open"]

        ).abs()

        lower_wick = (

            data[
                ["Open", "Close"]
            ].min(axis=1)

            -

            data["Low"]

        )

        signal = (

            lower_wick
            >
            body

        )

        return signal.fillna(
            False
        )

    # ==========================================
    # BREAKOUT
    # ==========================================
    if logic_type == "breakout":

        signal = (

            data["Close"]
            >
            data["PreviousHigh"]

        )

        return signal.fillna(
            False
        )

    # ==========================================
    # REACTION ZONE
    # ==========================================
    if logic_type == "zone":

        signal = (

            data["Close"]
            >
            data["Support"]

        )

        return signal.fillna(
            False
        )

    # ==========================================
    # LIQUIDITY SWEEP
    # ==========================================
    if logic_type == "liquidity":

        signal = (

            data["Low"]
            <
            data["PreviousLow"]

        )

        return signal.fillna(
            False
        )

    return None