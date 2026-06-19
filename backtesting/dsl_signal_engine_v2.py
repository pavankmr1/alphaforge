from backtesting.dsl_executor import (
    execute_rule
)


def generate_directional_signals(
    compiled_entry_logic,
    data
):

    long_entries = None
    long_exits = None

    for item in compiled_entry_logic:

        dsl = item.get(
            "dsl"
        )

        if not dsl:
            continue

        rules = dsl.get(
            "rules",
            []
        )

        for rule in rules:

            signal = execute_rule(
                rule,
                data
            )
            print()
            if signal is None:
                continue

            signal = (
                signal
                .fillna(False)
                .astype(bool)
            )
            rule_type = rule.get(
                "type"
            )

            # =====================
            # LONG ENTRY RULES
            # =====================
            if rule_type in [
                "cross_above",
                "trend_up"
            ]:

                if long_entries is None:

                    long_entries = signal

                else:

                    long_entries = (
                        long_entries
                        |
                        signal
                    )

            # =====================
            # LONG EXIT RULES
            # =====================
            elif rule_type in [
                "cross_below",
                "trend_down"
            ]:

                if long_exits is None:

                    long_exits = signal

                else:

                    long_exits = (
                        long_exits
                        |
                        signal
                    )

    # =====================
    # SAFE DEFAULTS
    # =====================
    if long_entries is None:

        long_entries = (
            data["Close"]
            > 999999999
        )

    if long_exits is None:

        long_exits = (
            data["Close"]
            > 999999999
        )

    long_entries = (
        long_entries
        .fillna(False)
        .astype(bool)
    )

    long_exits = (
        long_exits
        .fillna(False)
        .astype(bool)
    )

    # print(
    #     "FINAL ENTRY DTYPE:",
    #     long_entries.dtype
    # )

    # print(
    #     "FINAL EXIT DTYPE:",
    #     long_exits.dtype
    # )
    if long_entries is None:
        return None, None
    return (
        long_entries,
        long_exits
    )