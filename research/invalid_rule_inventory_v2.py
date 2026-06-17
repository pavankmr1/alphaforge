from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

left_counter = Counter()
right_counter = Counter()
type_counter = Counter()

for file in STRATEGY_DIR.glob(
    "*.json"
):

    try:

        strategy = json.loads(
            file.read_text()
        )

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

                if (
                    rule.get(
                        "validation_status"
                    )
                    !=
                    "invalid"
                ):
                    continue

                left = rule.get(
                    "left"
                )

                right = rule.get(
                    "right"
                )

                rule_type = rule.get(
                    "type"
                )

                if left:

                    left_counter[
                        left
                    ] += 1

                if right:

                    right_counter[
                        right
                    ] += 1

                if rule_type:

                    type_counter[
                        rule_type
                    ] += 1

    except Exception:
        pass

print()
print("=" * 60)
print("INVALID LEFT OPERANDS")
print("=" * 60)

for value, count in left_counter.most_common(
    30
):

    print(
        f"{value}: {count}"
    )

print()
print("=" * 60)
print("INVALID RIGHT OPERANDS")
print("=" * 60)

for value, count in right_counter.most_common(
    30
):

    print(
        f"{value}: {count}"
    )

print()
print("=" * 60)
print("INVALID RULE TYPES")
print("=" * 60)

for value, count in type_counter.most_common():

    print(
        f"{value}: {count}"
    )