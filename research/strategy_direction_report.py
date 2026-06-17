from pathlib import Path
import json

TARGET = (
    "EMA Crossover Trading Strategy"
)

for file in Path(
    "data/compiled_strategies_v3"
).glob("*.json"):

    try:

        strategy = json.loads(
            file.read_text()
        )

        if strategy.get(
            "name"
        ) != TARGET:

            continue

        print()
        print("=" * 60)
        print(strategy["name"])
        print("=" * 60)

        for item in strategy.get(
            "compiled_entry_logic",
            []
        ):

            print()

            print(
                "CONDITION:"
            )

            print(
                item.get(
                    "original_condition"
                )
            )

            dsl = item.get(
                "dsl"
            )

            if dsl:

                print(
                    "DSL:"
                )

                for rule in dsl.get(
                    "rules",
                    []
                ):

                    print(rule)

    except Exception:
        pass