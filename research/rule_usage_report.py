from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

left_counter = Counter()
right_counter = Counter()

strategy_count = 0
rule_count = 0

for file in STRATEGY_DIR.glob("*.json"):

    strategy_count += 1

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

        dsl = item.get(
            "dsl"
        )

        if not dsl:
            continue

        for rule in dsl.get(
            "rules",
            []
        ):

            rule_count += 1

            left = rule.get(
                "left"
            )

            right = rule.get(
                "right"
            )

            if left:

                left_counter[
                    left
                ] += 1

            if right:

                right_counter[
                    right
                ] += 1

print()
print("=" * 60)
print("INDICATOR USAGE REPORT")
print("=" * 60)

print()
print(
    "Strategies:",
    strategy_count
)

print(
    "Rules:",
    rule_count
)

print()

print("=" * 60)
print("TOP LEFT OPERANDS")
print("=" * 60)

for name, count in left_counter.most_common(30):

    print(
        f"{name}: {count}"
    )

print()

print("=" * 60)
print("TOP RIGHT OPERANDS")
print("=" * 60)

for name, count in right_counter.most_common(30):

    print(
        f"{name}: {count}"
    )

print()

print("=" * 60)
print("COMBINED INDICATOR USAGE")
print("=" * 60)

combined = Counter()

for k, v in left_counter.items():

    combined[k] += v

for k, v in right_counter.items():

    combined[k] += v

for name, count in combined.most_common(50):

    print(
        f"{name}: {count}"
    )