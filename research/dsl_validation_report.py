from pathlib import Path
from collections import Counter
import json

DATA_DIR = Path(
    "data/compiled_strategies_v2"
)

counter = Counter()

valid = 0
invalid = 0

for file in DATA_DIR.glob("*.json"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    for item in strategy.get(
        "compiled_entry_logic",
        []
    ):

        dsl = item.get(
            "dsl",
            {}
        )

        for rule in dsl.get(
            "rules",
            []
        ):

            status = rule.get(
                "validation_status",
                "unknown"
            )

            counter[status] += 1

            if status == "valid":
                valid += 1

            if status == "invalid":
                invalid += 1


print()

print("=" * 40)

print(
    f"Valid Rules: {valid}"
)

print(
    f"Invalid Rules: {invalid}"
)

total = valid + invalid

if total > 0:

    print(
        f"Quality Score: "
        f"{100 * valid / total:.2f}%"
    )

print("=" * 40)