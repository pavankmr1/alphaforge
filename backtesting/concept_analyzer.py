from agents.compiler.compiler_rules import (
    RULE_MAPPINGS
)

from loguru import logger


def analyze_unknown_conditions(
    strategy_data
):

    entry_conditions = strategy_data.get(
        "entry_conditions",
        []
    )

    unknown_conditions = []

    for condition in entry_conditions:

        condition_lower = (
            condition.lower()
        )

        matched = False

        for phrase in RULE_MAPPINGS:

            if phrase in condition_lower:

                matched = True
                break

        if not matched:

            unknown_conditions.append(
                condition
            )

    return unknown_conditions