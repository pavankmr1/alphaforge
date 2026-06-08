from formula_registry import (
    FORMULA_REGISTRY
)

from loguru import logger


def generate_signals(
    compiled_logic,
    data
):

    all_signals = []

    for item in compiled_logic:

        rules = item.get(
            "compiled_logic",
            []
        )

        for rule in rules:

            formula = rule.get(
                "formula"
            )

            signal_function = (
                FORMULA_REGISTRY.get(
                    formula
                )
            )

            if signal_function:

                logger.info(
                    f"Executing formula: "
                    f"{formula}"
                )

                signal = signal_function(
                    data
                )

                all_signals.append(
                    signal
                )

    return all_signals