from pathlib import Path
import json

for file in Path(
    "data/compiled_strategies_v3"
).glob("*.json"):

    try:

        strategy = json.loads(
            file.read_text()
        )

        rule_types = []

        for item in strategy.get(
            "compiled_entry_logic",
            []
        ):

            dsl = item.get(
                "dsl"
            )

            if not dsl:
                continue

            for rule in dsl.get(
                "rules",
                []
            ):

                if (
                    rule.get(
                        "validation_status"
                    )
                    ==
                    "valid"
                ):

                    rule_types.append(
                        rule["type"]
                    )

        has_long_short = (

            (
                "cross_above"
                in rule_types
            )
            and
            (
                "cross_below"
                in rule_types
            )

        ) or (

            (
                "trend_up"
                in rule_types
            )
            and
            (
                "trend_down"
                in rule_types
            )

        ) or (

            (
                "price_above"
                in rule_types
            )
            and
            (
                "price_below"
                in rule_types
            )

        )

        if has_long_short:

            print(
                file.name
            )

    except Exception:
        pass