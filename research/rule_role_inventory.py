from pathlib import Path
import json

STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

ENTRY_TYPES = {
    "cross_above",
    "cross_below"
}

FILTER_TYPES = {
    "trend_up",
    "trend_down",
    "price_above",
    "price_below",
    "volume_above",
    "greater_than",
    "less_than"
}

entry_counts = {}
filter_counts = {}
other_counts = {}

strategy_count = 0

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

            rule_type = rule.get(
                "type"
            )

            if not rule_type:
                continue

            # =====================
            # ENTRY RULES
            # =====================

            if rule_type in ENTRY_TYPES:

                entry_counts[
                    rule_type
                ] = (
                    entry_counts.get(
                        rule_type,
                        0
                    )
                    + 1
                )

            # =====================
            # FILTER RULES
            # =====================

            elif rule_type in FILTER_TYPES:

                filter_counts[
                    rule_type
                ] = (
                    filter_counts.get(
                        rule_type,
                        0
                    )
                    + 1
                )

            # =====================
            # OTHER
            # =====================

            else:

                other_counts[
                    rule_type
                ] = (
                    other_counts.get(
                        rule_type,
                        0
                    )
                    + 1
                )

print()
print("=" * 60)
print("RULE ROLE INVENTORY")
print("=" * 60)

print()
print(
    "Strategies:",
    strategy_count
)

print()

print("=" * 60)
print("ENTRY RULES")
print("=" * 60)

for k, v in sorted(
    entry_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"{k}: {v}"
    )

print()

print("=" * 60)
print("FILTER RULES")
print("=" * 60)

for k, v in sorted(
    filter_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"{k}: {v}"
    )

print()

print("=" * 60)
print("OTHER RULES")
print("=" * 60)

for k, v in sorted(
    other_counts.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"{k}: {v}"
    )