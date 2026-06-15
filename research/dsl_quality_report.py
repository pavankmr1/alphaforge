from pathlib import Path
from collections import Counter
import json

COMPILED_DIR = Path(
    "data/compiled_strategies_v2"
)

INVALID_FIELDS = {
    "Market",
    "Price",
    "Trend",
    "Setup",
    "Confirmation",
    "Time",
    "Timeframe"
}

field_counter = Counter()

total_strategies = 0
total_rules = 0
invalid_rules = 0

for file in COMPILED_DIR.glob("*.json"):

    total_strategies += 1

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    for condition in strategy.get(
        "compiled_entry_logic",
        []
    ):

        dsl = condition.get(
            "dsl",
            {}
        )

        rules = dsl.get(
            "rules",
            []
        )

        for rule in rules:

            total_rules += 1

            left = rule.get("left")
            right = rule.get("right")

            if left in INVALID_FIELDS:

                invalid_rules += 1
                field_counter[left] += 1

            if right in INVALID_FIELDS:

                invalid_rules += 1
                field_counter[right] += 1

print("\n===== DSL QUALITY REPORT =====")
print(
    f"Strategies: {total_strategies}"
)

print(
    f"Total Rules: {total_rules}"
)

print(
    f"Invalid Rules: {invalid_rules}"
)

coverage = (
    (total_rules - invalid_rules)
    / total_rules
) * 100

print(
    f"DSL Quality: {coverage:.2f}%"
)

print("\n===== TOP INVALID FIELDS =====")

for field, count in field_counter.most_common():

    print(
        f"{field}: {count}"
    )