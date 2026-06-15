from pathlib import Path
from collections import Counter
import json

counter = Counter()

for file in Path(
    "data/compiled_strategies_v2"
).glob("*.json"):

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

        dsl = item.get("dsl")

        if not dsl:
            continue

        for rule in dsl.get(
            "rules",
            []
        ):

            counter[
                rule["type"]
            ] += 1

print()

print("=" * 40)

for k, v in counter.most_common():

    print(
        f"{k}: {v}"
    )

print("=" * 40)