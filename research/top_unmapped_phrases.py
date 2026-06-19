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
    except:
        continue

    for item in strategy.get(
        "compiled_entry_logic",
        []
    ):

        if item.get("dsl"):
            continue

        condition = item.get(
            "original_condition",
            "UNKNOWN"
        )

        counter[
            condition
        ] += 1

print()
print("=" * 60)
print("TOP UNMAPPED CONDITIONS")
print("=" * 60)

for cond, count in counter.most_common(30):

    print()
    print(f"[{count}] {cond}")