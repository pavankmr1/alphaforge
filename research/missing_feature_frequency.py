from pathlib import Path
import json
from collections import Counter

counter = Counter()

strategy_dir = Path(
    "data/compiled_strategies_v3"
)

for file in strategy_dir.glob("*.json"):

    try:

        strategy = json.loads(
            file.read_text()
        )

    except Exception:
        continue

    compiled_logic = strategy.get(
        "compiled_entry_logic",
        []
    )

    for item in compiled_logic:

        dsl = item.get("dsl")

        if not dsl:
            continue

        for rule in dsl.get(
            "rules",
            []
        ):

            for operand in [
                rule.get("left"),
                rule.get("right")
            ]:

                if operand:

                    counter[
                        operand
                    ] += 1

print()
print("=" * 60)
print("TOP OPERANDS")
print("=" * 60)

for name, count in counter.most_common(50):

    print(
        f"{name}: {count}"
    )