from loguru import logger

from backtesting.dsl_executor import (
    execute_rule
)


def generate_dsl_signals(
    compiled_entry_logic,
    data
):

    final_signal = None

    for item in compiled_entry_logic:

        dsl = item.get("dsl")

        if not dsl:
            continue

        rules = dsl.get("rules", [])

        for rule in rules:

            signal = execute_rule(
                rule,
                data
            )

            if signal is None:
                continue

            print(
                rule,
                "->",
                int(signal.sum())
            )

            if final_signal is None:

                final_signal = signal

            else:

                final_signal = (
                    final_signal
                    &
                    signal
                )

            print(
                "Remaining Signals:",
                int(final_signal.sum())
            )

    return final_signal