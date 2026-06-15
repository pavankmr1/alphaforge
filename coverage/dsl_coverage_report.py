from pathlib import Path
import json

COMPILED_DIR = Path(
    "data/compiled_strategies_v2"
)

total_conditions = 0
compiled_conditions = 0
failed_conditions = 0

for file in COMPILED_DIR.glob("*.json"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    conditions = strategy.get(
        "compiled_entry_logic",
        []
    )

    for condition in conditions:

        total_conditions += 1

        if condition.get("source") in [
            "rule_mapping",
            "cache",
            "llm"
        ]:

            compiled_conditions += 1

        else:

            failed_conditions += 1

coverage = (
    compiled_conditions /
    total_conditions
    * 100
) if total_conditions else 0

print()

print("=" * 40)

print(
    f"Total Conditions: "
    f"{total_conditions}"
)

print(
    f"Compiled: "
    f"{compiled_conditions}"
)

print(
    f"Failed: "
    f"{failed_conditions}"
)

print(
    f"Coverage: "
    f"{coverage:.2f}%"
)

print("=" * 40)