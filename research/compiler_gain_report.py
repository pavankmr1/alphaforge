from pathlib import Path
import json

strategy_dir = Path(
    "data/compiled_strategies_v3"
)

compiled = 0
total = 0

for file in strategy_dir.glob("*.json"):

    try:
        strategy = json.loads(
            file.read_text()
        )

    except Exception:
        continue

    logic = strategy.get(
        "compiled_entry_logic",
        []
    )

    total += len(logic)

    for item in logic:

        if item.get("dsl"):

            compiled += 1

print()
print("=" * 60)
print("COMPILER PROGRESS")
print("=" * 60)

print(
    "Compiled:",
    compiled
)

print(
    "Total:",
    total
)

print(
    "Coverage:",
    round(
        compiled / total * 100,
        2
    ) if total else 0
)