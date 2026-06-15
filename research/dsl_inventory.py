from pathlib import Path
from collections import Counter
import json

DSL_DIR = Path(
    "data/compiled_strategies_v2"
)

counter = Counter()

for file in DSL_DIR.glob("*.json"):

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
            "dsl"
        )

        if not dsl:
            continue

        rules = dsl.get(
            "rules",
            []
        )

        for rule in rules:

            counter[
                rule.get(
                    "type"
                )
            ] += 1

print()

for k, v in counter.most_common():

    print(
        f"{k}: {v}"
    )