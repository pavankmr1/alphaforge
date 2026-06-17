import pandas as pd


def generate_exits(
    entries,
    data,
    strategy
):

    strategy_name = (
        strategy.get(
            "name",
            ""
        )
        .lower()
    )

    # ==========================================
    # EMA STRATEGIES
    # ==========================================
    if "ema" in strategy_name:

        if (
            "EMA9" in data.columns
            and
            "EMA20" in data.columns
        ):

            exits = (

                data["EMA9"]
                <
                data["EMA20"]

            )

            return exits.fillna(
                False
            ).astype(bool)

    # ==========================================
    # VWAP STRATEGIES
    # ==========================================
    if "vwap" in strategy_name:

        exits = (

            data["Close"]
            <
            data["VWAP"]

        )

        return exits.fillna(
            False
        ).astype(bool)

    # ==========================================
    # DEFAULT
    # ==========================================
    exits = (
        entries.shift(5)
        .fillna(False)
        .astype(bool)
    )

    return exits