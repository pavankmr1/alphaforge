from pathlib import Path
import json

shown = 0

for file in Path(
    "data/compiled_strategies_v3"
).glob("*.json"):

    strategy = json.loads(
        file.read_text()
    )

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
                "invalid"
            ):

                print()
                print("=" * 60)
                print(file.name)
                print(rule)

                shown += 1

                if shown >= 30:
                    raise SystemExit