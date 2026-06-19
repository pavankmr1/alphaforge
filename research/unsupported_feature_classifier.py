from pathlib import Path
import json
from collections import Counter

strategy_dir = Path(
    "data/compiled_strategies_v3"
)

counter = Counter()

for file in strategy_dir.glob("*.json"):

    try:
        strategy = json.loads(
            file.read_text()
        )
    except:
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
print("HIGH PRIORITY CANDIDATES")
print("=" * 60)

keywords = [

    "Zone",
    "Demand",
    "Supply",
    "Block",
    "Pivot",
    "POI",
    "Session",
    "Swing",
    "Breakout",
    "Resistance",
    "Support",
    "Fibonacci"

]

for name, count in counter.most_common():

    if any(
        k.lower() in name.lower()
        for k in keywords
    ):

        print(
            f"{name}: {count}"
        )