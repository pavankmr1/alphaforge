from pathlib import Path
import json

total_strategies = 0

dsl_rules = 0
compiled_logic = 0
invalid_rules = 0

for file in Path(
    "data/compiled_strategies_v3"
).glob("*.json"):

    total_strategies += 1

    strategy = json.loads(
        file.read_text()
    )

    for item in strategy.get(
        "compiled_entry_logic",
        []
    ):

        if item.get("dsl"):

            rules = item[
                "dsl"
            ].get(
                "rules",
                []
            )

            dsl_rules += len(
                rules
            )

            for rule in rules:

                if rule.get(
                    "validation_status"
                ) == "invalid":

                    invalid_rules += 1

        compiled_logic += len(
            item.get(
                "compiled_logic",
                []
            )
        )

print()
print("=" * 50)
print("CORPUS COVERAGE")
print("=" * 50)

print(
    f"Strategies: {total_strategies}"
)

print(
    f"DSL Rules: {dsl_rules}"
)

print(
    f"Compiled Logic: {compiled_logic}"
)

print(
    f"Invalid Rules: {invalid_rules}"
)